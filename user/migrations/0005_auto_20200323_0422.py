# Generated by Django 3.0 on 2020-03-22 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200322_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_additional_info',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
