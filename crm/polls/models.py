from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
QUESTIONTYPES = (
        ('mch', 'Multiple Choice'),
        ('chc', 'Choice'),
        ('txt', 'Text'),
        ('pck', 'Pick from list'),
        ('dat', 'Date')

        )
COMPANY_LOCATIONS = (
    ('WAW', 'Warszawa'),
    ('KRK', 'Kraków'),
    ('PZN', 'Poznań'),
    ('ALL',"All"),
    )
DEPARTAMENTS = (
    ('sal', 'Sales'),
    ('mar', 'Marketing'),
    ('HR', 'Human Resources'),
    ('ALL',"All"),
    )
class Poll(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User',on_delete=models.PROTECT)
    title =  models.CharField(max_length=200)
    published_date = models.DateTimeField(default=None,null = True, blank = True)
    target_departament = models.CharField(max_length=3, choices=DEPARTAMENTS,default='ALL')
    target_location = models.CharField(max_length=3, choices=COMPANY_LOCATIONS,default='ALL')
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey('polls.Poll',on_delete=models.CASCADE,null=True,blank=True,related_name='questions')
    title = models.TextField(max_length=200)
    order = models.IntegerField(null=True,blank=True)
    # textanswer = models.TextField(max_length=200,null=True,blank=True)
    # answer = models.OneToManyField('polls.Answer',blank=True,Null=True)
    enabletext = models.BooleanField(default=False)
    type = models.CharField(max_length=3, choices=QUESTIONTYPES,default='chc')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['order']

class Answer(models.Model):
    body = models.TextField(max_length=200)
    question = models.ForeignKey('polls.Question',on_delete=models.CASCADE,related_name='answers')


# class PollFinishFlag(models.Model):
#     user = models.ManyToManyField('auth.User')
#     poll = models.ManyToManyField('polls.Poll')
#     finished = models.BooleanField(default=False)


class PollSubmition(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    poll = models.ForeignKey('polls.Poll',on_delete=models.CASCADE,related_name='submitions')
    date = models.DateTimeField(default=timezone.now)

class PollSubmitionQuestion(models.Model):
    submition = models.ForeignKey('polls.PollSubmition',on_delete=models.CASCADE,related_name='submitions')
    question = models.ForeignKey('polls.Question',on_delete=models.CASCADE,related_name='submitions')
    # answer = models.ForeignKey('polls.Answer',on_delete=models.CASCADE,related_name='submitions',null=True,blank=True)
    answer = models.TextField(max_length=200)
    text = models.TextField(max_length=200,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    order = models.IntegerField(null=True,blank=True)
    def ans(self):
        if self.answer != None:
            return self.answer
        if self.text != None:
            return self.text
        if self.date != None:
            return self.date
