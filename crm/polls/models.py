from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.choices.choices import *
from django.template.defaultfilters import slugify

class Poll(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField(default=None, null=True, blank=True)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='non')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='non')
    slug = models.SlugField(max_length=20,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('polls:create_poll_answer', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[0:20])
        super(Poll, self).save(*args, **kwargs)


class Question(models.Model):
    poll = models.ForeignKey('polls.Poll', on_delete=models.CASCADE,
                             null=True, blank=True, related_name='questions')
    title = models.CharField(max_length=200)
    order = models.IntegerField(null=True, blank=True)
    enabletext = models.BooleanField(default=False)
    type = models.CharField(max_length=3, choices=QUESTIONTYPES, default='chc')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Answer(models.Model):
    body = models.TextField(max_length=200)
    question = models.ForeignKey(
        'polls.Question', on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.body


class PollSubmition(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    poll = models.ForeignKey(
        'polls.Poll', on_delete=models.CASCADE, related_name='submitions')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.username + " " + self.poll.title)


class PollSubmitionQuestion(models.Model):
    submition = models.ForeignKey(
        'polls.PollSubmition', on_delete=models.CASCADE, related_name='submitions')
    question = models.ForeignKey(
        'polls.Question', on_delete=models.CASCADE, related_name='submitions')
    manyanswer = models.ManyToManyField(
        'polls.Answer', related_name='submitions', blank=True)
    answer = models.TextField(max_length=200, null=True, blank=True)
    text = models.TextField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    def ans(self):
        if self.answer != None and self.text == None:

            return str(self.answer)
        elif self.answer != None and self.text is not None:
            return str(self.answer + "; " + self.text)
        elif self.text is not None:
            return str(self.text)
        elif self.date:
            return self.date.strftime("%m/%d/%Y")

    def __str__(self):
        return str(self.ans())
