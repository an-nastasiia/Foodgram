from rest_framework import mixins, viewsets, permissions
from users.models import User, Subscription
from . import serializers
from .viewsets import CreateListDestroyViewSet
from djoser import views
from django.shortcuts import get_object_or_404


class UserViewSet(views.UserViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)


class SubscriptionViewSet(CreateListDestroyViewSet):
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        if self.action == 'list':
            return get_object_or_404(User, pk=self.request.user.id).subscriber
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, author=get_object_or_404(
            User, pk=self.kwargs.get('author_id')))
