from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings
from accounts.choises import *

class AvatarManager(models.Manager):
    def resize_file(self, file):
        name, ext = os.path.splitext(file.name)
        format_ext_dict = {'.jpg': 'JPEG', '.png': 'PNG', '.gif': 'GIF'}
        img_format = format_ext_dict[ext]
        im = Image.open(file)
        im.thumbnail((128, 128), Image.ANTIALIAS)
        save_name = settings.MEDIA_DIR + '/profile_pics/' + name + ext
        im.save(fp=save_name, format=img_format)
        return save_name


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userprofile"
    )

    profile_pic = models.ImageField(
        upload_to='profile_pics',
        default='profile_pics/default-profile.png',
        blank=True
    )

    name = models.TextField(max_length=200)
    telephone = models.IntegerField()
    email = models.TextField(max_length=200, null=True)
    date_of_employement = models.DateTimeField(default=timezone.now)
    employee_id = models.CharField(max_length=20)
    position = models.CharField(max_length=40, default="")
    objects = AvatarManager()

    departament = models.CharField(
        max_length=3,
        choices=DEPARTAMENTS,
        default='non'
    )

    location = models.CharField(
        max_length=3,
        choices=COMPANY_LOCATIONS,
        default='non'
    )

    def __str__(self):
        return self.name
