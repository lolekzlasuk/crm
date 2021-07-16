import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os
from django.conf import settings
from accounts.choices.choices import *

class AvatarManager(models.Manager):
    def resize_file(self, file):
        name, ext = os.path.splitext(file.name)
        print(name + "  " + ext)
        format_ext_dict = {'.jpg': 'JPEG', '.png': 'PNG', '.gif': 'GIF'}
        img_format = format_ext_dict[ext]
        im = Image.open(file)
        im.thumbnail((128, 128), Image.ANTIALIAS)
        save_name = settings.MEDIA_DIR + '/profile_pics/' + name + ext
        im.save(fp=save_name, format=img_format)
        print(save_name)
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

    name = models.CharField(max_length=30)
    telephone = models.PositiveIntegerField()
    email = models.EmailField(max_length=50)
    date_of_employement = models.DateField(default=timezone.now)
    employee_id = models.PositiveIntegerField()
    position = models.CharField(max_length=40, default="trainee")
    objects = AvatarManager()
    first_login_string = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs):
        profiles = UserProfile.objects.order_by('-employee_id')
        highest_id = profiles[0].employee_id
        self.employee_id = highest_id + 1
        self.first_login_string = ''.join(random.choices( \
            string.ascii_letters + string.digits, k=15))
        super(UserProfile, self).save(*args, **kwargs)


    class Meta:
        ordering = ['employee_id']

    def set_default_profile_pic(self):
        if self.profile_pic != "profile_pics/default-profile.png":
            try:
                if os.path.isfile(self.profile_pic.path):
                    os.remove(self.profile_pic.path)
            except:
                pass
            self.profile_pic = "profile_pics/default-profile.png"
            self.save()


    def change_profile_pic(self,file):
        prev_pic = self.profile_pic
        image = UserProfile.objects.resize_file(file)
        self.profile_pic = image
        self.save()
        try:
            if (prev_pic != "profile_pics/default-profile.png" and
                prev_pic != self.profile_pic):
                if os.path.isfile(prev_pic.path):
                    os.remove(prev_pic.path)
        except:
            pass
