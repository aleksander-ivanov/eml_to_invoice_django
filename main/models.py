from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    country = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
