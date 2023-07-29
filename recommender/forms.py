from django import forms
from .models import Movie


class MoviePreferencesForm(forms.Form):
    TYPES = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show')
    ]

    movies_with_genre = Movie.objects.exclude(genre__isnull=True)
    GENRES = sorted(set(genre for movie in movies_with_genre for genre in movie.genre.split(', ')))
    GENRES.remove('TV Shows')
    genre = forms.MultipleChoiceField(choices=[(genre, genre) for genre in GENRES],
                                      widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=False)

    movies_with_release_year = Movie.objects.exclude(year__isnull=True)
    RELEASE_YEARS = sorted(set(movie.year for movie in movies_with_release_year),
                           reverse=True)
    release_year = forms.MultipleChoiceField(choices=[(year, year) for year in RELEASE_YEARS],
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                             required=False)

    movies_with_country = Movie.objects.exclude(country__isnull=True)
    COUNTRIES = sorted(set(country.strip() for movie in movies_with_country for country in movie.country.split(',')))
    COUNTRIES = [country for country in COUNTRIES if country]
    country = forms.MultipleChoiceField(choices=[(country, country) for country in COUNTRIES],
                                        widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=False)

    type = forms.ChoiceField(choices=TYPES, widget=forms.RadioSelect)
