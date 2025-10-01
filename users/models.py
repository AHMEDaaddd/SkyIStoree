from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Логиним по email, username оставляем, но он не используется как логин.
    """
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=64, blank=True)

    # Авторизация по email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # username оставляем обязательным полем для админки

    def __str__(self) -> str:
        return self.email or self.username