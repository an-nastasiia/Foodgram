from django.urls import include, path
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register('recipes', views.RecipeViewSet, basename='recipe')
router_v1.register('tags', views.TagViewSet, basename='tag')
router_v1.register('ingredients', views.IngredientViewSet,
                   basename='ingredient')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', views.SubscriptionViewSet.as_view(
        {'get': 'list'}), name='subscription'),
    path('users/<int:id>/subscribe/', views.SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='subscribe'),
    path('recipes/<int:id>/favorite/', views.FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='favorite'),
    path('recipes/<int:id>/shopping_cart/', views.ShoppingCartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='shopping-cart'),
    path('recipes/download_shopping_cart/', views.ShoppingCartViewSet.as_view(
        {'get': 'download_shopping_cart'}), name='download_cart'),
    path('', include('djoser.urls.base')),
    path('', include(router_v1.urls)),
]
