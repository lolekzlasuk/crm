from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
STATES = (
        ('acc', 'Accepted'),
        ('rej', 'Rejected'),
        ('wai', 'Awaiting'),
    )


class BoardCategory(models.Model):
    title = models.TextField(max_length=25)
    icon = models.TextField(blank=True)


    def __str__(self):
        return self.title

class Question(models.Model):
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User',on_delete=models.PROTECT)
    title =  models.CharField(max_length=200)
    answered = models.BooleanField(default=False)
    viewed_by = models.ManyToManyField('auth.User',related_name='viewer')
    category = models.ForeignKey('suggestions.BoardCategory',on_delete=models.PROTECT, related_name="qpa")
    last_answer = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


class Answer(models.Model):
    Question = models.ForeignKey('suggestions.Question',on_delete=models.CASCADE, related_name="answer")
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User',on_delete=models.PROTECT)

    def __str__(self):
        return self.body[0:20]
