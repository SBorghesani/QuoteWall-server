from django.db import models
from django.contrib.auth.models import User

class ApprovalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    status = models.BooleanField(default=False)