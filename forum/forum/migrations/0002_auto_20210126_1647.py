# Generated by Django 3.1.5 on 2021-01-26 16:47

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        UnaccentExtension()
    ]
