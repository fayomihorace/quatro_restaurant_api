"""API models module."""
from django.db import models
from django.contrib.auth.models import User


class UserApiKey(models.Model):
    """User ApiKey model Class."""
    user = models.OneToOneField(User, null=True, on_delete = models.PROTECT) 
    public_key = models.CharField(null=False, max_length=50)
    secret_key = models.CharField(null=False, max_length=50)

    class Meta:
        verbose_name = "user's keys"

    def __str__(self):
        return "{}.{}".format(self.public_key, self.secret_key)


class Restaurant(models.Model):
    """Restaurant model Class."""
    name = models.CharField(null=False, max_length=50)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)

    class Meta:
        verbose_name = "Restaurant"
        ordering = ['name']

    def __str__(self):
        return self.name
