# Generated by Django 3.1.1 on 2021-05-26 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_auto_20210526_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollsubmitionquestion',
            name='manyanswer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitions', to='polls.answer'),
        ),
    ]
