from colorfield.serializers import ColorField
from django.forms import ValidationError
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from rest_framework import serializers, validators
from users.models import Subscription, User


class CreateUserSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        requires_context = True

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Subscription.objects.filter(user=self.context['request'].user,
                                           author=obj).exists()


class ChangePasswordSerializer(djoser_serializers.SetPasswordSerializer):
    class Meta:
        model = User
        fields = ('new_password', 'current_password')
        write_only_fields = ('new_password', 'current_password')


class GetTokenSerializer(djoser_serializers.TokenCreateSerializer):
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('password', 'email')


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
    )

    class Meta:
        fields = ('user', 'id')
        model = Subscription
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'id'),
                message=('Вы уже подписаны на этого автора.')
            ),
        )

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise ValidationError('Нельзя подписаться на себя.')
        return data

    def to_representation(self, instance):
        data = SubscriptionSerializer(
            instance.author,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class UnsubscribeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
    )

    class Meta:
        fields = ('user', 'id')
        model = Subscription

    def validate(self, data):
        if not Subscription.objects.get(
            user=self.context['request'].user,
            id=self.context['request'].parser_context.get('kwargs').get('id')
                ).exists():
            raise ValidationError(
                'Нельзя отписаться от автора, на которого вы не подписаны.'
                )
        return data


class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class ShortRecipeSerializer(serializers.ModelSerializer):
    name = serializers.MultipleChoiceField(choices='db.recipes_ingredient.name')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    color = ColorField()

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeTagsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all()
    )

    class Meta:
        fields = ('id',)
        model = RecipeTag


class WriteRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class GetRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient

    # Этим методом удается получить данные amount, но все равно не понятно,
    # почему это значение нужно добывать через метод, если в Meta указана
    # модель RecipeIngredient. Если не прописывать amount = ..., то ошибка такая:
    #
    # Got AttributeError when attempting to get a value for field `amount` on serializer `GetRecipeIngredientSerializer`.
    # The serializer field might be named incorrectly and not match any attribute or key on the `Ingredient` instance.
    # Original exception text was: 'Ingredient' object has no attribute 'amount'.
    def get_amount(self, obj):
        return obj.ingredient_recipe.values_list('amount', flat=True).first()


class WriteRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = WriteRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'ingredients', 'tags', 'author',
            'image', 'name', 'text', 'cooking_time'
        )
        model = Recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient['id'],
                                            amount=ingredient['amount'])
        return recipe

    def update(self, instance, validated_data):
        m2m_fields = ('tags', 'ingredients')
        for attr, value in validated_data.items():
            if attr not in m2m_fields:
                setattr(instance, attr, value)
        instance.save()

        instance.tags.set(validated_data.get('tags'))

        get_ingredients = validated_data.pop('ingredients')
        post_ingredients = []
        print('INGREDIENTS:', get_ingredients)
        for ingredient in get_ingredients:
            print('INGREDIENT:', ingredient)
            print('INSTANCE:', instance)
            print('AMOUNT:', ingredient['amount'])
            recipe_ingredient = RecipeIngredient.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            print('recipe_ingredient:', recipe_ingredient)
            post_ingredients.append(recipe_ingredient[0].ingredient)
        instance.ingredients.set(post_ingredients)
        return instance

    def to_representation(self, instance):
        print('INSTANCE !!!:', instance)
        data = GetRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        print('DATA:', data)
        return data


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = GetRecipeIngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=self.context['request'].user, recipe=obj
            ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context['request'].user, recipe=obj
            ).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        fields = ('user', 'id')
        model = Favorite
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'id'),
                message=('Этот рецепт уже в избранном.')
            ),
        )

    def to_representation(self, instance):
        data = ShortRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'user', 'recipe')
        model = ShoppingCart
