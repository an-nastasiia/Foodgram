from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, RecipeTag, RecipeIngredient


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredient)
