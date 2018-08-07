from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings

__all__ = (
    'User',
)


class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
