# Generated by Django 3.1.1 on 2021-06-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_auto_20210615_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]