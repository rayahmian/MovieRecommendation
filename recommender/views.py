from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import unquote
import json
import pandas as pd
from .models import Movie
from .forms import MoviePreferencesForm
from Data.data import df


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

            # Convert the recommendation_data to JSON and encode it in the URL
            encoded_recommendation_data = json.dumps(recommendation_data)
            return HttpResponseRedirect(reverse('show_recommendations', args=[encoded_recommendation_data]))

    else:
        form = MoviePreferencesForm()

    return render(request, 'movie_preferences.html', {
        'form': form,
        'genre_choices': genre_choices,
        'release_year_choices': release_year_choices,
        'country_choices': country_choices
    })


def show_recommendations(request, encoded_recommendation_data):
    # Decode the URL parameter
    decoded_recommendation_data = unquote(encoded_recommendation_data)
    recommendation_data = json.loads(decoded_recommendation_data)

    return render(request, 'recommendations.html', {'recommendations': recommendation_data})
