# Generated by Django 3.1.5 on 2021-02-12 07:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0004_auto_20210212_0551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='raiting',
        ),
        migrations.RemoveField(
            model_name='section',
            name='raiting',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='raiting',
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Likers'),
        ),
        migrations.AddField(
            model_name='section',
            name='likers',
            field=models.ManyToManyField(related_name='liked_sections', to=settings.AUTH_USER_MODEL, verbose_name='Likers'),
        ),
        migrations.AddField(
            model_name='thread',
            name='likers',
            field=models.ManyToManyField(related_name='liked_threads', to=settings.AUTH_USER_MODEL, verbose_name='Likers'),
        ),
    ]