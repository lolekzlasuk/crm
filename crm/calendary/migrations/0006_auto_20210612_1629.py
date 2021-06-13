# Generated by Django 2.2.3 on 2021-06-12 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendary', '0005_devent_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devent',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calendary.Day'),
        ),
        migrations.AlterField(
            model_name='devent',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='devent',
            name='end',
            field=models.TimeField(default='23:59'),
        ),
        migrations.AlterField(
            model_name='devent',
            name='start',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AlterField(
            model_name='devent',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
