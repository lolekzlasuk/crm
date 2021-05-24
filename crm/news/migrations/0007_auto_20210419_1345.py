# Generated by Django 2.2.3 on 2021-04-19 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0006_auto_20210415_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='docquestion',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='docquestion',
            name='answer',
            field=models.TextField(blank=True, default=None, max_length=5000),
        ),
    ]
