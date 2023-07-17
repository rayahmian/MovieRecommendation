from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    platform = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    director = models.CharField(max_length=100, null=True, blank=True)
    cast = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    genre = models.CharField(max_length=400)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
