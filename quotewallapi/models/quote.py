from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name='groups')
    quote_text = models.CharField(max_length=200)
    quoter = models.CharField(max_length=50)
    context = models.CharField(max_length=200)
    date_added = models.DateField(auto_now=False, auto_now_add=False)