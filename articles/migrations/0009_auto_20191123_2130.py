# Generated by Django 2.1.7 on 2019-11-23 18:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0008_auto_20191123_2128'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dilike',
            new_name='Dislike',
        ),
    ]
