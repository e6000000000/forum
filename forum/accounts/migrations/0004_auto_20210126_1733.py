# Generated by Django 3.1.5 on 2021-01-26 17:33

from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210126_1620'),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension(),
    ]
