from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Day(models.Model):
    date = models.DateField()

class Devent(models.Model):
    day = models.ForeignKey('calendary.Day',on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=5000)
    start = models.TimeField(default="00:00")
    end = models.TimeField(default="23:59")
    author = models.ForeignKey('auth.user',on_delete=models.PROTECT)

    def __str__(self):
        return self.title
