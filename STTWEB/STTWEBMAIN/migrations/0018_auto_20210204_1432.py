# Generated by Django 3.1.3 on 2021-02-04 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0017_auto_20210204_1432'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Channel',
            new_name='Channels',
        ),
        migrations.AlterField(
            model_name='videos',
            name='similar_videos_updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 4, 14, 32, 40, 923500)),
        ),
    ]