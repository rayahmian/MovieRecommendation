from django import forms


class MoviePreferencesForm(forms.Form):
    type = forms.CharField(max_length=50, required=False)
    genre = forms.CharField(max_length=100, required=False)
    release_year = forms.IntegerField(required=False)
    country = forms.CharField(max_length=100, required=False)
