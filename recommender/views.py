from django.shortcuts import render
from .models import Movie


def movie_list(request):
    # Get all movies from the database
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    # Get the movie with the given ID from the database
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})
