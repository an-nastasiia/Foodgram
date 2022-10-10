from ast import Sub
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User, Subscription
from recipes.models import Recipe
from . import serializers
from .viewsets import CreateListDestroyViewSet, CreateDestroyViewSet
from djoser import views
from django.shortcuts import get_object_or_404, get_list_or_404


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
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
        print('QUERYSET', queryset)
        return [obj.author for obj in queryset]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        obj = get_object_or_404(Subscription, user=self.request.user,
                                author=self.kwargs.get('id'))
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer


class FavoriteViewSet(CreateDestroyViewSet):
    pass
