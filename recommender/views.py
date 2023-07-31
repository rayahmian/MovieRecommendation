import random
from django.shortcuts import render
from django.db.models import Q
from recommender.forms import MoviePreferencesForm
from recommender.models import Movie


def generator(request):
    if request.method == 'POST':
        form = MoviePreferencesForm(request.POST)
        if form.is_valid():
            selected_platforms = form.cleaned_data['platform']
            selected_genres = form.cleaned_data['genre']
            selected_release_years = form.cleaned_data['release_year']
            selected_countries = form.cleaned_data['country']

            # Filter movies based on selected attributes
            movies = Movie.objects.all()
            if selected_platforms:
                platform_query = Q()
                for platform in selected_platforms:
                    platform_query |= Q(platform__contains=platform)
                movies = movies.filter(platform_query)
            if selected_genres:
                genre_query = Q()
                for genre in selected_genres:
                    genre_query |= Q(genre__contains=genre)
                movies = movies.filter(genre_query)
            if selected_release_years:
                movies = movies.filter(year__in=selected_release_years)
            if selected_countries:
                country_query = Q()
                for country in selected_countries:
                    country_query |= Q(country__contains=country)
                movies = movies.filter(country_query)
            total_movies = movies.count()
            if total_movies <= 3:
                recommendations = list(movies)
            else:
                recommendations = random.sample(list(movies), 3)
            for movie in recommendations:
                if movie.duration:
                    movie.duration = int(round(float(movie.duration)))

            return render(request, 'results.html', {'recommendations': recommendations})

    else:
        form = MoviePreferencesForm()

    return render(request, 'generator.html', {'form': form})


def results(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        genre = request.POST.get('genre')
        release_year = request.POST.get('release_year')
        country = request.POST.get('country')

        filtered_movies = Movie.objects.filter(platform=platform, genre=genre, year=release_year, country=country)

        if filtered_movies.exists():
            num_recommendations = 3
            recommendations = random.sample(list(filtered_movies), min(num_recommendations, len(filtered_movies)))
            return render(request, 'results.html', {'recommendations': recommendations})

    return render(request, 'results.html', {'recommendations': []})
