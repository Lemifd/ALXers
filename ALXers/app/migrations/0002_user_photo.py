# Generated by Django 3.2.18 on 2023-04-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='app/static/profiles/abeny.jpeg', upload_to='app/static/profiles'),
        ),
    ]
