from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class User(AbstractUser):
    """
    A custom User model
    """
    bio = models.TextField()
    avatar = ResizedImageField(
        size=[250, 250],
        crop=['middle', 'center'],
        force_format='PNG',
        upload_to='avatars',
        default='default.png'
    )