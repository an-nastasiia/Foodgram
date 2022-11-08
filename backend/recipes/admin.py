from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart, Tag)


class AtLeastOneFormSet(BaseInlineFormSet):
    def clean(self):
        super(AtLeastOneFormSet, self).clean()
        non_empty_forms = 0
        for form in self:
            if form.cleaned_data:
                non_empty_forms += 1
        if non_empty_forms - len(self.deleted_forms) < 1:
            raise ValidationError('Добавьте хотя бы один элемент.')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_per_page = 15
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    list_per_page = 15
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    formset = AtLeastOneFormSet


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeTagInline, RecipeIngredientInline]
    list_display = ('pk', 'name', 'author', 'in_favorited')
    list_filter = ('author', 'name', 'tags')
    list_per_page = 15
    empty_value_display = '-пусто-'

    @admin.display(description='Добавлено в избранное')
    def in_favorited(self, obj):
        return f'{Favorite.objects.filter(recipe=obj).count()} раз'


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
