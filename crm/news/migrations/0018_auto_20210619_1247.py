# Generated by Django 3.1.1 on 2021-06-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_auto_20210619_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsfile',
            name='extension',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]