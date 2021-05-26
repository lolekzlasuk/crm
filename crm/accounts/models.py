from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
import os
from django.core.validators import FileExtensionValidator
from django.conf import settings
# Create your models here.

class AvatarManager(models.Manager):
    def resize_file(self,file):
        print(file.name)
        name, ext = os.path.splitext(file.name)
        format_ext_dict = {'.jpg':'JPEG','.png':'PNG','.gif':'GIF'}
        img_format = format_ext_dict[ext]
        print('avatar')
        im = Image.open(file)
        print(im.size)
        im.thumbnail((128,128),Image.ANTIALIAS)
        print(im.size)
        save_name = settings.MEDIA_DIR + '/profile_pics/' + name + ext
        im.save(fp=save_name,format=img_format)
        print('saved')
        print(save_name)




        return save_name

class UserProfile(models.Model):
    COMPANY_LOCATIONS = (
        ('WAW', 'Warszawa'),
        ('KRK', 'Kraków'),
        ('PZN', 'Poznań'),
        ('non',"None"),
        )
    DEPARTAMENTS = (
        ('sal', 'Sales'),
        ('mar', 'Marketing'),
        ('HR', 'Human Resources'),
        ('non',"None"),
        )
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile")
    profile_pic = models.ImageField(upload_to='profile_pics',default='profile_pics/default-profile.png',blank=True)
    name = models.TextField(max_length=200)
    telephone = models.IntegerField()
    email = models.TextField(max_length=200,null=True)
    date_of_employement = models.DateTimeField(default=timezone.now)
    employee_id = models.CharField(max_length=20)
    vacation_status = models.BooleanField(default=False)
    departament = models.CharField(max_length=3, choices=DEPARTAMENTS,default='non')
    location = models.CharField(max_length=3, choices=COMPANY_LOCATIONS,default='non')
    position  = models.CharField(max_length=40,default="")
    objects = AvatarManager()

    def __str__(self):
        return self.user.username

class Vacation(models.Model):
    start_date= models.DateTimeField(default=None)
    end_date= models.DateTimeField(default=None)
    user= models.ForeignKey('auth.User',on_delete=models.PROTECT)
