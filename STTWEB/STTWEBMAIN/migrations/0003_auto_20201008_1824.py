# Generated by Django 3.1.2 on 2020-10-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STTWEBMAIN', '0002_searches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='downloaded',
            field=models.IntegerField(default=0),
        ),
    ]