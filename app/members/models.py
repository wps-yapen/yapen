from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user',blank=True)
    CHOICE_GENDER=(
        ('m','남성'),
        ('f','여성'),
        ('x','선텍안함'),
    )

    img_profile = models.ImageField(upload_to='user',  blank= True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank= True)
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER,null=True)

    def __str__(self):
        return self.username
