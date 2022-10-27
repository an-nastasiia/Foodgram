from django.db.models import Count
from django.contrib import admin

from .models import (Tag, Ingredient, Recipe, Favorite, ShoppingCart,
                     RecipeTag, RecipeIngredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_per_page = 15
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'in_favorited')
    list_filter = ('author', 'name', 'tags')
    list_per_page = 15
    empty_value_display = '-пусто-'

    @admin.display(description='Добавлено в избранное')
    def in_favorited(self, obj):
        return f'{Favorite.objects.filter(recipe=obj).count()} раз'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    list_per_page = 15
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
    list_per_page = 15
    empty_value_display = '-пусто-'


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    list_editable = ('recipe', 'tag')
    list_per_page = 15
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient')
    list_editable = ('recipe', 'ingredient')
    list_per_page = 15
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
    list_per_page = 15
    empty_value_display = '-пусто-'
