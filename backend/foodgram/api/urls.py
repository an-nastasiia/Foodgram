from django.urls import include, path
from rest_framework import routers
from . import views
from djoser.views import TokenCreateView, TokenDestroyView


router_v1 = routers.DefaultRouter()
router_v1.register(r'^users?', views.UserViewSet, basename='user')
router_v1.register(r'^users/subscriptions?',
                   views.SubscriptionViewSet, basename='subscription')
router_v1.register(r'^users/(?P<author_id>\d+)/subscribe?',
                   views.SubscriptionViewSet, basename='subscribe')


urlpatterns = [
    path('auth/token/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls))
]
