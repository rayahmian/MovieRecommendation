from django.shortcuts import render
import pandas as pd
from .models import Movie
from .forms import MoviePreferencesForm
from Data.data import df


def movie_list(request):
    # Get all movies from the database
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


def movie_detail(request, movie_id):
    # Get the movie with the given ID from the database
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})


def recommend_movies(request):
    genre_choices = set()
    country_choices = set()

    df['genre'] = df['genre'].astype(str)

    for genres in df['genre']:
        genre_choices.update(genre.strip() for genre in genres.split(','))
    for countries in df['country']:
        if isinstance(countries, str) and not pd.isna(countries):
            countries_list = [country.strip() for country in countries.split(',') if country.strip()]
            country_choices.update(countries_list)

    genre_choices = sorted(list(genre_choices))
    country_choices = sorted(list(country_choices))
    release_year_choices = sorted(df['release_year'].unique(), reverse=True)

    if request.method == 'POST':
        form = MoviePreferencesForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_type = form.cleaned_data['type']
            user_genre = form.cleaned_data['genre']
            user_release_year = form.cleaned_data['release_year']
            user_country = form.cleaned_data['country']

            # DEBUG
            print(form.cleaned_data)

            # Logic to filter movies
            filtered_df = df.copy()
            if user_type:
                filtered_df = filtered_df[filtered_df['type'] == user_type]
            if user_genre:
                filtered_df = filtered_df[filtered_df['genre'].apply(lambda x: any(item in x for item in user_genre))]
            if user_release_year:
                filtered_df = filtered_df[filtered_df['release_year'].isin(user_release_year)]
            if user_country:  # Check if the user selected any countries
                filtered_df = filtered_df[
                    filtered_df['country'].apply(lambda x: any(item in x for item in user_country))]

            # Handle case when no movies match the user's criteria
            if filtered_df.empty:
                message = "No movies found matching your preferences."
                return render(request, 'movie_preferences.html', {'form': form, 'message': message})

            # Logic to generate 5 random movies
            num_recommendations = 5
            recommendations = filtered_df.sample(n=num_recommendations)
            recommendation_data = recommendations[['title', 'genre']].to_dict(orient='records')
            return render(request, 'recommendations.html', {
                'recommendations': recommendation_data,
                'user_type': user_type,
                'user_genre': user_genre,
                'user_release_year': user_release_year,
                'user_country': user_country,
                'genre_choices': genre_choices,
                'release_year_choices': release_year_choices,
                'country_choices': country_choices
            })
        else:
            # DEBUG
            print(form.errors)
    else:
        form = MoviePreferencesForm()

    return render(request, 'movie_preferences.html', {
        'form': form,
        'genre_choices': genre_choices,
        'release_year_choices': release_year_choices,
        'country_choices': country_choices
    })
