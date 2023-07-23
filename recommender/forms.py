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
        # Replace 'df' with your DataFrame containing the genre data
        # Assuming the genre column in your DataFrame is 'genre'
        genres = df['genre'].unique()
        return [(genre, genre) for genre in genres]

    def get_release_year_choices(self):
        # Replace 'df' with your DataFrame containing the release_year data
        # Assuming the release_year column in your DataFrame is 'release_year'
        release_years = df['release_year'].unique()
        return [(year, year) for year in release_years]

    def get_country_choices(self):
        # Replace 'df' with your DataFrame containing the country data
        # Assuming the country column in your DataFrame is 'country'
        countries = df['country'].unique()
        return [(country, country) for country in countries]
