# Generated by Django 3.1.1 on 2021-06-30 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devent',
            name='day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='calendary.day'),
        ),
    ]
