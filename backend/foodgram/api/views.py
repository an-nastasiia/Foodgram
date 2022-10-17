from django.shortcuts import get_object_or_404
from djoser import views
from recipes.models import Favorite, Ingredient, Recipe, Tag, ShoppingCart
from rest_framework import permissions, viewsets
from users.models import Subscription, User

from . import serializers
from .viewsets import (CreateDestroyViewSet, CreateListDestroyViewSet,
                       ListRetrieveViewSet)


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_classes = {'GET': serializers.UserSerializer,
                          'POST': serializers.CreateUserSerializer}

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_classes.get(self.request.method)
        print('self.request.method:', self.request.method)
        print('serializer_class:', serializer_class)
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class SubscriptionViewSet(CreateListDestroyViewSet):
    serializer_classes = {'create': serializers.SubscribeSerializer,
                          'list': serializers.SubscriptionSerializer,
                          'destroy': serializers.UnsubscribeSerializer}

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        queryset = self.request.user.subscriber.all()
        return [obj.author for obj in queryset]

    def get_object(self):
        obj = get_object_or_404(Subscription, user=self.request.user,
                                author=self.kwargs.get('id'))
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.GetRecipeSerializer
        return serializers.WriteRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = serializers.FavoriteSerializer

    def get_queryset(self):
        queryset = self.request.user.user_favorite.all()
        return [obj.recipe for obj in queryset]

    def get_object(self):
        obj = get_object_or_404(Favorite, user=self.request.user,
                                recipe=self.kwargs.get('id'))
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingCartViewSet(CreateDestroyViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = serializers.ShoppingCartSerializer
