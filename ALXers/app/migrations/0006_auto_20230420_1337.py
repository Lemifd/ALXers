# Generated by Django 3.2.18 on 2023-04-20 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_user_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='dob',
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=23),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='male', max_length=255),
            preserve_default=False,
        ),
    ]