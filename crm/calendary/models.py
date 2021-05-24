from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Day(models.Model):
    date = models.DateField()

class Devent(models.Model):
    day = models.ForeignKey('calendary.Day',on_delete=models.PROTECT)
    title = models.TextField()
    description = models.TextField(blank=True,null=True)
    start = models.TimeField(default=0)
    end = models.TimeField(blank=True,null=True)
    author = models.ForeignKey('auth.user',on_delete=models.PROTECT)
