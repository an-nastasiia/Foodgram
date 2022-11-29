from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'tag name',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        'color in HEX',
        format='hex',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'ingredient name',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'measurement unit',
        max_length=200,
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='tags',
        related_name='tags',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='recipe_author',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='ingredients',
        related_name='ingredient',
    )
    name = models.CharField(
        'name',
        max_length=200,
    )
    image = models.ImageField(
        'image',
        upload_to='media/recipes/',
    )
    text = models.TextField(
        'description',
        max_length=1500,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'cooking time',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(240)
        )
    )

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='recipe',
        on_delete=models.CASCADE,
        related_name='recipe_tag'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='tag',
        on_delete=models.CASCADE,
        related_name='tag_recipe'
    )

    class Meta:
        verbose_name = 'tag of recipe'
        verbose_name_plural = 'tags of recipe'
        ordering = ('-pk',)

    def __str__(self):
        return f'tag {self.tag.slug} of recipe {self.recipe.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='recipe',
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ingredient',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        'amount',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(2500)
        )
    )

    class Meta:
        verbose_name = 'recipe`s ingredient'
        verbose_name_plural = 'recipes` ingredients'
        ordering = ('-pk',)

    def __str__(self):
        return f'ingredient {self.ingredient.name} in {self.recipe.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='user_favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='recipe',
        related_name='recipe_favorite'
    )

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                name='no_double_favorite',
                fields=('user', 'recipe'),
            )
        ]

    def __str__(self):
        return f'{self.recipe.name} is favorited by {self.user.username}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='cart_user'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='recipe',
        on_delete=models.CASCADE,
        related_name='cart_recipe'
    )

    class Meta:
        verbose_name = 'shopping list'
        verbose_name_plural = 'shopping lists'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                name='no_double_add_to_shopping_cart',
                fields=('user', 'recipe'),
            )
        ]

    def __str__(self):
        return f'{self.recipe.name} in shopping list of {self.user.username}'
