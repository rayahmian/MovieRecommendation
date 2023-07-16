from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=500)
    year = models.IntegerField()
    platform = models.CharField(max_length=20)



