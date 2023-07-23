from django import forms
from MovieRecommendation.data import df


class MoviePreferencesForm(forms.Form):
    TYPE_CHOICES = (
        ('TV Show', 'TV Show'),
        ('Movie', 'Movie'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)
    genre = forms.MultipleChoiceField(choices=[], required=False)
    release_year = forms.MultipleChoiceField(choices=[], required=False)
    country = forms.MultipleChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].choices = self.get_genre_choices()
        self.fields['release_year'].choices = self.get_release_year_choices()
        self.fields['country'].choices = self.get_country_choices()

    def get_genre_choices(self):
        genre_concatenated = ','.join(df['genre'].dropna())
        all_genres = genre_concatenated.split(',')
        unique_genres = list(set(all_genres))
        # Create a list of tuples
        choices = [(genre, genre) for genre in unique_genres]
        return choices

    def get_release_year_choices(self):
        release_years = df['release_year'].unique()
        return [(year, year) for year in release_years]

    def get_country_choices(self):
        country_concatenated = ','.join(df['country'].dropna())
        all_countries = country_concatenated.split(',')
        unique_countries = list(set(all_countries))
        # Create a list of tuples
        countries = df['country'].unique()
        return [(country, country) for country in countries]
