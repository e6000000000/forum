# Generated by Django 3.1.5 on 2021-02-12 05:51

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210126_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='default.png', force_format='PNG', keep_meta=True, quality=0, size=[250, 250], upload_to='avatars', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email address'),
        ),
    ]