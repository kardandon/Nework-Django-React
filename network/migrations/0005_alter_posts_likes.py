# Generated by Django 3.2.5 on 2021-07-12 10:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_posts_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
