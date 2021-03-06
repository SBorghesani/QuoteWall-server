from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    members = models.ManyToManyField(User, through="UserGroup", related_name="member_of")
    requests = models.ManyToManyField(User, through="ApprovalRequest", related_name="requesting_to_join")