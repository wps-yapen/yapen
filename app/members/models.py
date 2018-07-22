from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)

    def __str__(self):
        return self.username
