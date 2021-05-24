# Generated by Django 2.2.3 on 2021-04-19 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20210419_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='docfile',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='news.KnowledgeCategory'),
        ),
        migrations.AddField(
            model_name='docquestion',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='news.KnowledgeCategory'),
        ),
        migrations.AddField(
            model_name='documentf',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='news.KnowledgeCategory'),
        ),
        migrations.DeleteModel(
            name='UserQuestion',
        ),
    ]
