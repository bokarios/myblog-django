# Generated by Django 2.1.7 on 2019-11-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.png', upload_to='post_pics'),
        ),
    ]
