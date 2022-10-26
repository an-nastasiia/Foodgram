from rest_framework.filters import SearchFilter
from django_filters.rest_framework.filterset import FilterSet
from django_filters import filters

from recipes.models import Favorite, Recipe, Ingredient, ShoppingCart, Tag


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


def filter_is_in(self, request):
    related_name = self._meta.model.recipe.related_name
    queryset = self.queryset
    if self.field_name == '1':
        recipes = user.related_name.values_list('recipe_id', flat=True)
        queryset = queryset.filter(pk__in=recipes)
    return queryset


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(field_name='is_favorited', method=filter_is_in)
    is_in_shopping_cart = filters.BooleanFilter(field_name='is_in_shopping_cart', method=filter_is_in)
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
