from rest_framework import serializers, validators
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
    is_subscribed = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')


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


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'author')
        model = Subscription
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author')),
        )

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise ValidationError('Нельзя подписаться на себя!')
        return data
