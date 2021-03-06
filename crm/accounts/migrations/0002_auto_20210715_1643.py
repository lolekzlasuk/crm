# Generated by Django 3.1.1 on 2021-07-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_login_string',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
