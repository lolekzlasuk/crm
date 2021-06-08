from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import UserProfile
# Create your models here.
import os
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.conf import settings
from accounts.choises import COMPANY_LOCATIONS,DEPARTAMENTS,QUESTIONTYPES,STATES


class FileManager(models.Manager):
    def save_file(self, file):
        file_to_save = self.create(file=file)
        name, ext = os.path.splitext(file.name)

        format_ext_dict = {'.jpg': 'JPEG', '.png': 'PNG', '.gif': 'GIF'}
        if ext in format_ext_dict.keys():
            file_to_save.extension = 'image'
            img_format = format_ext_dict[ext]
            print(img_format)
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
    staticdoc = models.BooleanField(default=False)
    files = models.ManyToManyField('news.NewsFile', default=None, blank=True)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='ALL')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='ALL')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        notif = Notification.objects.create(
            news=self,
            title="New news for you!",
            body=self.title[0:20]
        )
        audience = UserProfile.objects.all()
        if self.target_location != "ALL":
            audience = audience.filter(location=self.target_location)
        if self.target_departament != "ALL":
            audience = audience.filter(departament=self.target_departament)

        for each in audience:
            notifreadflag = NotificationReadFlag.objects.create(
                user=each.user,
                notification=notif
            )
            newsreadflag = NewsReadFlag.objects.create(
                user=each.user,
                news=self
            )

    def __str__(self):
        return self.title


class NewsFile(models.Model):
    file = models.FileField(upload_to='upload/%Y/%m/%d', default=None, blank=True, validators=[
                            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif', 'pdf'])])
    miniature = models.TextField(default=None, null=True, blank=True)
    extension = models.TextField(default=None, null=True, blank=True)
    isnews = models.BooleanField(default=True)
    objects = FileManager()
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='ALL')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='ALL')

    def __str__(self):
        return str(self.file.name.split("/")[-1])

    # @property
    # def file_type(self):
    #     name, extension = os.path.splitext(self.file.path)
    #     if extension in ['.jpg','.png','.gif']:
    #         return 'image'
    #     if extension == '.pdf':
    #         return 'pdf'
    #     return 'unknown'


class Notification(models.Model):
    news = models.ForeignKey('news', on_delete=models.CASCADE, default="0")
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class NotificationReadFlag(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    notification = models.ForeignKey(
        'news.Notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class NewsReadFlag(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)


class KnowledgeCategory(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class DocumentF(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    date_created = models.DateTimeField(default=timezone.now)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='ALL')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='ALL')
    category = models.ForeignKey(
        'news.KnowledgeCategory',
         on_delete=models.PROTECT,
         default=2,
         related_name="docs"
    )


class DocFile(models.Model):
    file = models.FileField(upload_to='documents')
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='ALL')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='ALL')
    category = models.ForeignKey(
        'news.KnowledgeCategory', on_delete=models.PROTECT,
         default=2, related_name="files"
    )


class DocQuestion(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    answer = models.TextField(
        max_length=5000, default=None, blank=True, null=True)
    target_departament = models.CharField(
        max_length=3, choices=DEPARTAMENTS, default='ALL')
    target_location = models.CharField(
        max_length=3, choices=COMPANY_LOCATIONS, default='ALL')
    date_created = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        'news.KnowledgeCategory', on_delete=models.PROTECT,
        default=2, related_name="questions"
    )


class UserQuestion(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    author = models.ForeignKey(
        'auth.User', on_delete=models.PROTECT, blank=True, null=True)
