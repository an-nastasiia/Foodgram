from django.urls import include, path
from rest_framework import routers
from . import views


router_v1 = routers.DefaultRouter()
router_v1.register(r'^users/?', views.UserViewSet, basename='user')
# router_v1.register(r'^users/subscriptions/?$',
#                    views.SubscriptionViewSet, basename='subscription')
# router_v1.register(r'^users/(?P<id>\d+)/subscribe/?$',
#                    views.SubscriptionViewSet, basename='subscribe')
router_v1.register(r'^recipes/?', views.RecipeViewSet, basename='recipe')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', views.SubscriptionViewSet.as_view(
        {'get': 'list'}), name='subscription'),
    path('users/<id>/subscribe/', views.SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}), name='subscribe'),
    path('', include(router_v1.urls))
]
