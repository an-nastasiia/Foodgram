from rest_framework import serializers

from recipes.models import Recipe
from users.models import User
from .default_for_fields import CurrentID


class EmbeddedRecipeSerializer(serializers.ModelSerializer):
    '''Serializer for Recipe model with less number of fields.'''

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class BaseSubscribeSerializer(serializers.ModelSerializer):
    '''Base serializer for Subscription model, write allowed.'''

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
    '''Base serializer for many-to-many User and Recipe models' relations.'''

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
