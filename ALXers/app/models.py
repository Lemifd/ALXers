from django.db import models

# Create your models here.

class User(models.Model):
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    age=models.IntegerField()
    gender=models.CharField(max_length=255)
    solved=models.IntegerField(default=0)
    submitted=models.IntegerField(default=0)
    photo=models.ImageField(upload_to='static/profiles/',default="")
    

    def __str__(self) -> str:
        return f"{self.fname}"

class Image(models.Model):
    photo=models.ImageField()
