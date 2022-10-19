from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from users.models import Subscription

from . import serializers
from .viewsets import CreateDestroyViewSet, CreateListDestroyViewSet


class SubscriptionViewSet(CreateListDestroyViewSet):
    serializer_classes = {'create': serializers.SubscribeSerializer,
                          'list': serializers.SubscriptionSerializer,
                          'destroy': serializers.UnsubscribeSerializer}
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def get_queryset(self):
        queryset = self.request.user.subscriber.all()
        return [obj.author for obj in queryset]

    def get_object(self):
        return get_object_or_404(Subscription, user=self.request.user,
                                 author=self.kwargs.get('id'))


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    lookup_url_kwarg = 'id'
    permission_classes = (CurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author')
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.GetRecipeSerializer
        return serializers.WriteRecipeSerializer


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = serializers.FavoriteSerializer
    queryset = Favorite.objects.all()

    def get_object(self):
        return get_object_or_404(Favorite, user=self.request.user,
                                 recipe_id=self.kwargs.get('id'))


class ShoppingCartViewSet(CreateDestroyViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = serializers.ShoppingCartSerializer

    def get_object(self):
        return get_object_or_404(ShoppingCart, user=self.request.user,
                                 recipe_id=self.kwargs.get('id'))

    def get_ingredients_list(self):
        recipes_in_cart = Recipe.objects.filter(
            cart_recipe__user=self.request.user).values_list(
                'ingredients__name',
                'recipe_ingredient__amount',
                'ingredients__measurement_unit'
            )
        user_cart = recipes_in_cart.values(
            'ingredients__name', 'ingredients__measurement_unit').annotate(
                total=Sum('recipe_ingredient__amount')).order_by('-total')
        return user_cart

    @action(detail=False)
    def download_shopping_cart(self, request):
        cart = self.get_ingredients_list()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"'
            )
        pdfmetrics.registerFont(TTFont('RadioVolna', 'RadioVolna.ttf'))
        pdf = canvas.Canvas(response)
        pdf.setFont('RadioVolna', 25)
        pdf.drawString(
            150, 800, f'{request.user.first_name}, не забудь купить:'
            )
        pdf.setFont('RadioVolna', 20)
        pdf.translate(cm, 26.5*cm)
        for item in range(len(cart)):
            pdf.drawString(
                100, -item*cm,
                (f"{item+1}) {cart[item].get('ingredients__name')} - "
                 f"{cart[item].get('total')} "
                 f"{cart[item].get('ingredients__measurement_unit')};")
                )
        pdf.showPage()
        pdf.save()
        return response
