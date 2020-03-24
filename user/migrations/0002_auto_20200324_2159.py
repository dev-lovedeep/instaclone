# Generated by Django 3.0 on 2020-03-24 16:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_additional_info',
            name='follower',
            field=models.ManyToManyField(blank=True, default=None, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user_additional_info',
            name='following',
            field=models.ManyToManyField(blank=True, default=None, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
