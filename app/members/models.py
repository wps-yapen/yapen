from django.contrib.auth.models import AbstractUser
from django.db import models

__all__ = (
    'User',
)

class User(AbstractUser):
    class Meta:
        db_table = "users"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.email
