from rest_framework import serializers

from recipes.models import Recipe
from users.models import User
from .default_for_fields import CurrentID


class EmbeddedRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Recipe с меньшим числом полей.'''

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class BaseSubscribeSerializer(serializers.ModelSerializer):
    '''Базовый сериализатор для модели Subscription с возможностью записи.'''

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    id = serializers.PrimaryKeyRelatedField(
        source='author',
        queryset=User.objects.all(),
        default=CurrentID(User)
    )


class BaseUserRecipeSerializer(serializers.ModelSerializer):
    '''Базовый сериализатор для many-to-many связей моделей User и Recipe.'''

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        source='recipe',
        default=CurrentID(Recipe)
    )

    def create(self, validated_data):
        user = validated_data.get('user')
        id = validated_data.get('id')
        return self.Meta.model.objects.create(
            user=user,
            recipe=id
        )

    def to_representation(self, instance):
        return EmbeddedRecipeSerializer(
            instance.recipe,
            context={
                'request': self.context.get('request')
            }
        ).data
