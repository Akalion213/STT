# Generated by Django 3.1.3 on 2020-11-25 20:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0014_auto_20201118_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videos',
            name='tags_2',
        ),
        migrations.RemoveField(
            model_name='videos',
            name='tags_3',
        ),
        migrations.RemoveField(
            model_name='videos',
            name='tags_4',
        ),
        migrations.AlterField(
            model_name='videos',
            name='similar_videos_updated',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 22, 16, 45, 771280)),
        ),
        migrations.AlterField(
            model_name='videos',
            name='subtitles_checked',
            field=models.DateTimeField(default='2010-01-01 12:00:00'),
        ),
    ]