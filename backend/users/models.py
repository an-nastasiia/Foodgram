from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """User model."""

    email = models.EmailField(
        'email',
        )
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        'name',
        max_length=150,
    )
    last_name = models.CharField(
        'last name',
        max_length=150,
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('pk',)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='subscriber',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscriptions',
        verbose_name='author',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                name='no_double_subscribe',
                fields=('user', 'author'),
            ),
            models.CheckConstraint(
                name='no_self_subscribe',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def clean(self):
        if self.author == self.user:
            raise ValidationError('You can not subscribe to yourself')

    def __str__(self):
        return f'{self.user.username} is subscribed to {self.author.username}'
