from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    CreatedOn = models.DateField(auto_now=False, auto_now_add=False)