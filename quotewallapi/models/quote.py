from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name='groups')
    quote_text = models.TextField()
    quoter = models.CharField(max_length=100)
    context = models.TextField()
    date_added = models.DateField(auto_now=False, auto_now_add=False)