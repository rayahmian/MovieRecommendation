from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    platform = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    director = models.CharField(max_length=100)
    cast = models.CharField(max_length=200)
    rating = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    genre = models.CharField(max_length=400)
    description = models.TextField()
