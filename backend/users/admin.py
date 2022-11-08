from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import Subscription, User


admin.site.site_header = 'Foodgram Admin'
admin.site.index_title = 'Разделы'
admin.site.site_title = 'Администрирование Foodgram'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')
    list_filter = ('username', 'email')
    list_per_page = 15
    search_fields = ('username', 'first_name', 'last_name')
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_per_page = 15
    search_fields = ('user', 'author')
    empty_value_display = '-пусто-'
