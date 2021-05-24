# Generated by Django 3.1.1 on 2020-10-10 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201010_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.poll'),
        ),
    ]
