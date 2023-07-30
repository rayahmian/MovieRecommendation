from django import forms
from .models import Movie


class MoviePreferencesForm(forms.Form):

    # GENRES
    movies_with_genre = Movie.objects.exclude(genre__isnull=True)
    GENRES = sorted(set(genre for movie in movies_with_genre for genre in movie.genre.split(', ')))
    GENRES.remove('TV Shows')
    GENRES.remove('Movies')
    GENRES.remove('Series')
    genre = forms.MultipleChoiceField(
        choices=[(genre, genre) for genre in GENRES],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    # RELEASE YEARS
    movies_with_release_year = Movie.objects.exclude(year__isnull=True)
    RELEASE_YEARS = sorted(set(movie.year for movie in movies_with_release_year),
                           reverse=True)
    release_year = forms.MultipleChoiceField(
        choices=[(year, year) for year in RELEASE_YEARS],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    # COUNTRIES
    movies_with_country = Movie.objects.exclude(country__isnull=True)
    COUNTRIES = sorted(set(country.strip() for movie in movies_with_country for country in movie.country.split(',')))
    COUNTRIES = [country for country in COUNTRIES if country]
    country = forms.MultipleChoiceField(
        choices=[(country, country) for country in COUNTRIES],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    # PLATFORMS
    movies_with_platform = Movie.objects.exclude(platform__isnull=True)
    PLATFORMS = sorted(
        set(platform.strip() for movie in movies_with_platform for platform in movie.platform.split(',')))
    PLATFORMS = [platform for platform in PLATFORMS if platform]
    platform = forms.MultipleChoiceField(
        choices=[(platform, platform) for platform in PLATFORMS],
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
