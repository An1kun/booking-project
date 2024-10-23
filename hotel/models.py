from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='hotel_images/')


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)



