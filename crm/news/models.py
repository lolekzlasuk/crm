from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserProfile
import os
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.conf import settings
from accounts.choices.choices import *
from django.urls import reverse
from django.template.defaultfilters import slugify


class FileManager(models.Manager):
    def save_file(self, file):
        file_to_save = self.create(file=file)
        name, ext = os.path.splitext(file.name)
        format_ext_dict = {'.jpg': 'JPEG', '.png': 'PNG', '.gif': 'GIF'}
        if ext in format_ext_dict.keys():
            file_to_save.extension = 'image'
            img_format = format_ext_dict[ext]
            size = 128, 128
            im = Image.open(file)
            im.thumbnail(size)
            thumbnail_name = settings.THUMBNAILS_DIR + name + "-thumb" + ext
            im.save(thumbnail_name, format=img_format)
            file_to_save.miniature = "/media/upload/thumbs/" + name + "-thumb" + ext

        if ext == '.pdf':
            file_to_save.extension = 'pdf'

        return file_to_save


class News(models.Model):

    body = models.TextField(max_length=5000)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    published_date = models.DateTimeField(default=None, null=True, blank=True)
    files = models.ManyToManyField('news.NewsFile', default=None, blank=True)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='non')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='non')
    slug = models.SlugField(max_length=20)

    def create_notifications(self):
        notification_instance = Notification.objects.create(
            news=self,
            title="New news for you!",
            body=self.title[0:20]
        )
        audience = UserProfile.objects.all()
        if self.target_location != "non":
            audience = audience.filter(location=self.target_location)
        if self.target_departament != "non":
            audience = audience.filter(departament=self.target_departament)

        for each in audience:
            notifreadflag = NotificationReadFlag.objects.create(
                user=each.user,
                notification=notification_instance

            )

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        self.create_notifications()

    def __str__(self):
        return self.title[0:30]

    def get_absolute_url(self):
        return reverse('news:newsdetail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[0:20])
        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "news"
        ordering = ['-published_date', '-date_created', 'id']


class NewsFile(models.Model):
    file = models.FileField(upload_to='upload/%Y/%m/%d',
                            default=None,
                            blank=True,
                            validators=[
                                FileExtensionValidator(
                            allowed_extensions=['jpg', 'png', 'gif', 'pdf'])
                            ])

    miniature = models.TextField(default=None, null=True, blank=True,)
    extension = models.CharField(
        default=None, null=True, blank=True, max_length=10)
    objects = FileManager()

    def __str__(self):
        return str(self.file.name.split("/")[-1])

    def get_absolute_url(self):
        return self.file.url


class Notification(models.Model):
    news = models.ForeignKey('news', on_delete=models.CASCADE, default="0")
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body[0:20]


class NotificationReadFlag(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    notification = models.ForeignKey(
        'news.Notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return '{0} ({1}) '.format(self.user.userprofile, self.notification)


class KnowledgeCategory(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Knowledge Categories"


class DocumentF(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    date_created = models.DateTimeField(default=timezone.now)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='non')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='non')
    category = models.ForeignKey(
        'news.KnowledgeCategory',
        on_delete=models.PROTECT,
        default=2,
        related_name="docs"
    )

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:docdetail', args=[str(self.id)])


class DocFile(models.Model):
    file = models.FileField(upload_to='documents/%Y/%m/%d')
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='non')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='non')
    category = models.ForeignKey(
        'news.KnowledgeCategory', on_delete=models.PROTECT,
        default=2, related_name="files"
    )
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.file.url


class DocQuestion(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000, blank=True, null=True)
    answer = models.TextField(
        max_length=5000, default=None, blank=True, null=True)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='non')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='non')
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        'auth.User', on_delete=models.PROTECT, blank=True, null=True)
    category = models.ForeignKey(
        'news.KnowledgeCategory', on_delete=models.PROTECT,
        default=1, related_name="questions"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


# delte this
class UserQuestion(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    author = models.ForeignKey(
        'auth.User', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.title
