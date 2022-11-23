from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription, User
from . import serializers
from .filters import IngredientSearchFilter, RecipeFilter
from .generate_pdf import generate_pdf
from .permissions import IsAuthorOrAdminOrReadOnly
from .viewsets import CreateDestroyViewSet, CreateListDestroyViewSet


class SubscriptionViewSet(CreateListDestroyViewSet):
    '''Viewset for Subscription model.'''

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.SubscriptionSerializer
        return serializers.SubscribeSerializer

    def get_queryset(self):
        queryset = self.request.user.subscriber.all()
        return [obj.author for obj in queryset]

    def get_object(self):
        return get_object_or_404(Subscription, user=self.request.user,
                                 author=self.kwargs.get('id'))

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.kwargs.get('id'))
        serializer.save(user=self.request.user, id=author)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset for Tag model.'''

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset for Ingredient model.'''

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    '''Viewset for Recipe model.'''

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.GetRecipeSerializer
        return serializers.WriteRecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class FavoriteViewSet(CreateDestroyViewSet):
    '''Viewset for Favorite model.'''

    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Favorite, user=self.request.user,
                                 recipe_id=self.kwargs.get('id'))

    def perform_create(self, serializer):
        recipe_id = get_object_or_404(Recipe, pk=self.kwargs.get('id'))
        serializer.save(user=self.request.user, id=recipe_id)


class ShoppingCartViewSet(CreateDestroyViewSet):
    '''Viewset for ShoppingCart model.'''

    queryset = ShoppingCart.objects.all()
    serializer_class = serializers.ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(ShoppingCart, user=self.request.user,
                                 recipe_id=self.kwargs.get('id'))

    def perform_create(self, serializer):
        recipe_id = get_object_or_404(Recipe, pk=self.kwargs.get('id'))
        serializer.save(user=self.request.user, id=recipe_id)

    def get_ingredients_list(self):
        '''Transform recipes into a list of unique ingredients.'''
        recipes_in_cart = Recipe.objects.filter(
            cart_recipe__user=self.request.user).values_list(
                'ingredients__name',
                'recipe_ingredient__amount',
                'ingredients__measurement_unit'
            )
        return recipes_in_cart.values(
            'ingredients__name', 'ingredients__measurement_unit').annotate(
                total=Sum('recipe_ingredient__amount')).order_by('-total')

    def download_shopping_cart(self, request):
        '''Download shopping list as PDF-file.'''
        cart = self.get_ingredients_list()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"'
            )
        cart = self.get_ingredients_list()
        return generate_pdf(self, response, cart)
