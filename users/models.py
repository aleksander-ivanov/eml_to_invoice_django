from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):

    email = models.EmailField(unique=True, max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username
