from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField()


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


