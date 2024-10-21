from django.db import models
from users.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField()


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    content = models.TextField()
    stars = models.IntegerField()
