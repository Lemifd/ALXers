# Generated by Django 3.2.18 on 2023-04-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_image_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='', upload_to='static/profiles/'),
        ),
    ]
