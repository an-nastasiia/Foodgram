from rest_framework import serializers, validators, exceptions
from django.forms import ValidationError
from djoser import serializers as djoser_serializers
from users.models import User, Subscription
from recipes.models import Tag, Ingredient, Recipe, Favorite, RecipeTag, RecipeIngredient


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
        return Subscription.objects.filter(
            user=self.context['request'].user, author=obj).exists()


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


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe


class NestedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


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
        print("            I'M HEREEEEE            ")
        print(self.context['request'].parser_context.get('kwargs').get('id'))
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
        serializer = NestedRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite
