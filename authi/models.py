from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class todo(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    task = models.TextField(max_length=200)
    dat = models.DateField(default=date.today)
    select = models.TextField(max_length=250)
