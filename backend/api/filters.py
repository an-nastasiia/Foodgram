from django_filters import filters
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework.filters import BooleanFilter

from recipes.models import Recipe, Tag


class IngredientSearchFilter(SearchFilter):
    '''Filter for Ingredient model with search parameter "name".'''

    search_param = 'name'


class RecipeFilter(FilterSet):
    '''Filterset for four fields of Recipe model.'''

    is_favorited = BooleanFilter(method='filter_is_in')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in')
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_in(self, queryset, name, value):
        '''Method for filtering by search parameter values 0 and 1.'''
        user = self.request.user
        if user.is_authenticated and value:
            if name == 'is_favorited':
                return queryset.filter(recipe_favorite__user=user)
            elif name == 'is_in_shopping_cart':
                return queryset.filter(cart_recipe__user=user)
            else:
                raise f'Неизвестный параметр {name}'
        return queryset
