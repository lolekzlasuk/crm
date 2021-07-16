from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Day(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%m.%d.%Y')


class Devent(models.Model):
    day = models.ForeignKey(
        'calendary.Day', on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=5000)
    start = models.TimeField('Start time', default='00:00')
    end = models.TimeField('Ending time', default='23:59')
    author = models.ForeignKey('auth.user', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=20, null=True)

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.day)

    def get_absolute_url(self):
        return reverse('calendary:devent', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[0:20])
        super(Devent, self).save(*args, **kwargs)
