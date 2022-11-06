from django.forms import ValidationError
from djoser import serializers as djoser_serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from users.models import Subscription, User

from .base_serializers import (BaseSubscribeSerializer,
                               BaseUserRecipeSerializer,
                               EmbeddedRecipeSerializer)
from .validators import check_for_duplicates


class CreateUserSerializer(djoser_serializers.UserCreateSerializer):
    '''Сериализатор для создания объекта модели User.'''

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class UserSerializer(djoser_serializers.UserSerializer):
    '''Сериализатор для модели User.'''

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return (self.context['request'].user.is_authenticated
                and Subscription.objects.filter(
                user=self.context['request'].user, author=obj
                ).exists())


class ChangePasswordSerializer(djoser_serializers.SetPasswordSerializer):
    '''Сериализатор для изменения пароля учетной записи пользователя.'''

    class Meta:
        model = User
        fields = ('new_password', 'current_password')
        write_only_fields = ('new_password', 'current_password')


class GetTokenSerializer(djoser_serializers.TokenCreateSerializer):
    '''Сериализатор для получения токена авторизации.'''

    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('password', 'email')


class SubscribeSerializer(BaseSubscribeSerializer):
    '''Сериализатор для записи данных для модели Subscription.'''

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
        request = self.context['request']
        if request.method == 'POST' and request.user == data['author']:
            raise ValidationError('Нельзя подписаться на себя.')
        if request.method == 'DELETE' and not Subscription.objects.get(
            user=request.user,
            id=request.parser_context.get('kwargs').get('id')
        ):
            raise ValidationError(
                'Нельзя отписаться от автора, на которого вы не подписаны.'
            )
        return data

    def to_representation(self, instance):
        return SubscriptionSerializer(
            instance.author,
            context={
                'request': self.context.get('request')
                }
            ).data

    def create(self, validated_data):
        user = validated_data.get('user')
        id = validated_data.get('id')
        return Subscription.objects.create(user=user, author=id)


class SubscriptionSerializer(UserSerializer):
    '''Сериализатор для получения данных объектов модели Subscription.'''

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
        serializer = EmbeddedRecipeSerializer(recipes, many=True)
        try:
            recipes_limit = int(
                self.context['request'].query_params.get('recipes_limit')
            )
            return serializer.data[:recipes_limit]
        except TypeError:
            return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Ingredient.'''

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Tag.'''

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeTagsSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели RecipeTag.'''

    id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())

    class Meta:
        fields = ('id',)
        model = RecipeTag


class WriteRecipeIngredientsSerializer(serializers.ModelSerializer):
    '''Сериализатор для записи данных для модели RecipeIngredient.'''

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class GetRecipeIngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения данных для модели RecipeIngredient.'''

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class WriteRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для записи данных для модели Recipe.'''

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = UserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = WriteRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id', 'ingredients', 'tags', 'author',
            'image', 'name', 'text', 'cooking_time'
        )
        model = Recipe

    def validate_tags(self, value):
        for tag in value:
            if not Tag.objects.filter(id=tag.id).exists():
                raise ValidationError('Такого тега не существует.')
        if check_for_duplicates(value):
            raise ValidationError('Теги рецепта не должны повторяться.')
        return value

    def validate_ingredients(self, value):
        for ingredient in value:
            if not Ingredient.objects.filter(id=ingredient['id'].id).exists():
                raise ValidationError('Такого ингредиента не существует.')
        if check_for_duplicates(value):
            raise ValidationError('Ингредиенты рецепта не должны повторяться.')
        return value

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
        for ingredient in get_ingredients:
            recipe_ingredient = RecipeIngredient.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
            post_ingredients.append(recipe_ingredient[0].ingredient)
        instance.ingredients.set(post_ingredients)
        return instance

    def to_representation(self, instance):
        return GetRecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class GetRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения данных для модели Recipe.'''

    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True)

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe

    def get_ingredients(self, obj):
        return GetRecipeIngredientSerializer(
            obj.recipe_ingredient.all(), many=True).data

    def get_is_favorited(self, obj):
        return (self.context['request'].user.is_authenticated
                and Favorite.objects.filter(
                user=self.context['request'].user, recipe=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        return (self.context['request'].user.is_authenticated
                and ShoppingCart.objects.filter(
                user=self.context['request'].user, recipe=obj
                ).exists())


class FavoriteSerializer(BaseUserRecipeSerializer):
    '''Сериализатор для модели Favorite.'''

    class Meta:
        fields = ('user', 'id')
        model = Favorite


class ShoppingCartSerializer(BaseUserRecipeSerializer):
    '''Сериализатор для модели ShoppingCart.'''

    class Meta:
        fields = ('user', 'id')
        model = ShoppingCart
