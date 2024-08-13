from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=40, **NULLABLE, verbose_name="Телефон (Не обязательно)", help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars', **NULLABLE, verbose_name='Аватар (Не обязательно)',
                               help_text='Загрузите свой аватар')
    country = models.CharField(max_length=50, verbose_name='Страна (Обязательно)')

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
