from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        blank=False,
        null=False,
        )
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False,
    )
    is_subscribed = models.BooleanField(
        'Подписан ли текущий пользователь на этого пользователя',
        default=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscriptions',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('pk',)
        constraints = [
            models.UniqueConstraint(
                name='no_double_subscribe',
                fields=('user', 'author',),
            ),
            models.CheckConstraint(
                name='no_self_subscribe',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return self.user.username + ' подписан на ' + self.author.username
