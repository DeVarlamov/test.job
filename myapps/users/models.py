from django.db import models
from django.contrib.auth.models import AbstractUser

from myapps.settings import USER, TEACHER
from users.validate import validate_username


ROLE_CHOICES = [
    (USER, USER),
    (TEACHER, TEACHER),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=(validate_username,),
        help_text='введите username',
        error_messages={
            'unique': 'Юзернаме уже занят',
            },
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        error_messages={
            'unique': 'Почта уже занята',
        },
    )
    password = models.CharField('Пароль', max_length=30)
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)

    role = models.CharField(
        'роль',
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    @property
    def is_admin(self):
        return self.role == TEACHER or self.is_superuser

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
