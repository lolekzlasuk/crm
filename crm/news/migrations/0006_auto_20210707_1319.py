# Generated by Django 2.2.3 on 2021-07-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20210707_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='published_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
