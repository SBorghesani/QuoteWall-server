from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name='groups')
    quote_text = models.CharField(max_length=500)
    quoter = models.CharField(max_length=75)
    context = models.CharField(max_length=500)
    date_added = models.DateField(auto_now=False, auto_now_add=False)