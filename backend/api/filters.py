from rest_framework.filters import SearchFilter
from django_filters.rest_framework.filterset import FilterSet
from django_filters import filters

from recipes.models import Recipe, Tag


class IngredientSearchFilter(SearchFilter):
    '''Фильтр для модели Ingredient с параметром поиска name.'''

    search_param = 'name'


class RecipeFilter(FilterSet):
    '''Фильтрсет для модели Recipe по четырем полям.'''

    is_favorited = filters.BooleanFilter(method='filter_is_in')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in')
    author = filters.NumberFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_in(self, queryset, name, value):
        '''Метод для фильтрации по параметрам поиска со значениями 0 или 1.'''
        user = self.request.user
        if user.is_authenticated and value:
            if name == 'is_favorited':
                return queryset.filter(user_favorite__user=user)
            elif name == 'is_in_shopping_cart':
                return queryset.filter(cart_user__user=user)
        return queryset
