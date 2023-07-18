from django.core.management.base import BaseCommand
import pandas as pd
from recommender.models import Movie


class Command(BaseCommand):
    help = 'Seed the database with movie data from CSV'

    def handle(self, *args, **options):
        # Delete all existing records
        Movie.objects.all().delete()

        # Seed the new data
        df = pd.read_csv('movies_data.csv')

        for _, row in df.iterrows():
            title = row['title']
            year = row['release_year']
            platform = row['platform']
            type = row['type']
            director = row['director'] if not pd.isna(row['director']) else None
            cast = row['cast'] if not pd.isna(row['cast']) else None
            country = row['country'] if not pd.isna(row['country']) else None
            rating = row['rating'] if not pd.isna(row['rating']) else None
            duration = row['duration'] if not pd.isna(row['duration']) else None
            genre = row['listed_in']
            description = row['description'] if not pd.isna(row['description']) else None

            movie = Movie(
                title=title,
                year=year,
                platform=platform,
                type=type,
                director=director,
                cast=cast,
                country=country,
                rating=rating,
                duration=duration,
                genre=genre,
                description=description,
            )
            movie.save()

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
