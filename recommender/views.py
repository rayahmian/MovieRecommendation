import random
from django.shortcuts import render
from recommender.forms import MoviePreferencesForm
from recommender.models import Movie


def generator(request):
    if request.method == 'POST':
        form = MoviePreferencesForm(request.POST)
        if form.is_valid():
            selected_type = form.cleaned_data['type']
            selected_genres = form.cleaned_data['genre']
            selected_release_years = form.cleaned_data['release_year']
            selected_countries = form.cleaned_data['country']

            # Filter movies based on selected attributes
            movies = Movie.objects.all()
            if selected_type:
                movies = movies.filter(type=selected_type)
            if selected_genres:
                movies = movies.filter(genre__in=selected_genres)
            if selected_release_years:
                movies = movies.filter(year__in=selected_release_years)
            if selected_countries:
                movies = movies.filter(country__in=selected_countries)

            # Get the total number of available movies in the queryset
            total_movies = movies.count()

            if total_movies <= 5:
                # If there are 5 or fewer movies, return all available movies as recommendations
                recommendations = list(movies)
            else:
                # Randomly select 5 movies from the filtered queryset
                recommendations = random.sample(list(movies), 5)

            return render(request, 'results.html', {'recommendations': recommendations})
    else:
        form = MoviePreferencesForm()

    return render(request, 'generator.html', {'form': form})


def results(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        release_year = request.POST.get('release_year')
        country = request.POST.get('country')

        filtered_movies = Movie.objects.filter(genre=genre, year=release_year, country=country)

        if filtered_movies.exists():
            num_recommendations = 5
            # Number of movie recommendations to display
            recommendations = random.sample(list(filtered_movies), min(num_recommendations, len(filtered_movies)))
            return render(request, 'results.html', {'recommendations': recommendations})

    return render(request, 'results.html', {'recommendations': []})
