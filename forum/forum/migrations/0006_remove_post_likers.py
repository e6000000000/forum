# Generated by Django 3.1.5 on 2021-02-12 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20210212_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likers',
        ),
    ]