from django.core.management.base import BaseCommand
import pandas as pd
from recommender.models import Movie


class Command(BaseCommand):
    help = 'Seed the database with movie data from CSV'

    def handle(self, *args, **options):
        df = pd.read_csv('movies_data.csv')

        for _, row in df.iterrows():
            movie = Movie(
                title=row['title'],
                year=row['release_year'],
                platform=row['platform'],
                type=row['type'],
                director=row['director'],
                cast=row['cast'],
                rating=row['rating'],
                duration=row['duration'],
                genre=row['listed_in'],
                description=row['description']
            )
            movie.save()

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
