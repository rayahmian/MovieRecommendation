from genre_dict import genre_mapping
import pandas as pd
import numpy as np
import os


def remove_duplicate_genres(genre_string):
    g = genre_string.split(', ')
    ug = sorted(set(g), key=g.index)
    return ', '.join(ug)


# INITIALIZE THE DATA
file_pathA = os.path.join(os.path.dirname(__file__), 'amazonprime_data.csv')
file_pathD = os.path.join(os.path.dirname(__file__), 'disneyplus_data.csv')
file_pathH = os.path.join(os.path.dirname(__file__), 'hulu_data.csv')
file_pathN = os.path.join(os.path.dirname(__file__), 'netflix_data.csv')

adf = pd.read_csv(file_pathA)
ddf = pd.read_csv(file_pathD)
hdf = pd.read_csv(file_pathH)
ndf = pd.read_csv(file_pathN)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


# CLEAN THE DATA
# Add the "platform" column to each DataFrame
adf['platform'] = 'Amazon Prime'
ddf['platform'] = 'Disney Plus'
hdf['platform'] = 'Hulu'
ndf['platform'] = 'Netflix'

# Modify the show IDs
adf['show_id'] = 'AP' + adf['show_id'].str[1:]
ddf['show_id'] = 'DP' + ddf['show_id'].str[1:]
hdf['show_id'] = 'H' + hdf['show_id'].str[1:]
ndf['show_id'] = 'N' + ndf['show_id'].str[1:]

# Create a consolidated dataset using all 4 datasets
df1 = pd.concat([adf, ddf, hdf, ndf], ignore_index=True)
df1.rename(columns={'listed_in': 'genre'}, inplace=True)
column_order = ['title', 'show_id', 'type', 'platform', 'director', 'cast', 'country', 'date_added', 'release_year',
                'rating', 'duration', 'genre', 'description']
df1 = df1.reindex(columns=column_order)
# df1.info()


# EXPLORATORY DATA ANALYSIS
# Extract a string of countries movies were made in
df1['country'] = df1['country'].astype(str)
df_countries = df1['country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
df_countries = df_countries.str.strip()
df_countries = df_countries[df_countries != '']
unique_countries = df_countries.unique()
countries_string = ', '.join(unique_countries)
# print('Countries :' + countries_string)

# Extract a string of the genres available
df1['genre'] = df1['genre'].astype(str)
df_genres = df1['genre'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
df_genres = df_genres.str.strip()
unique_genres = df_genres.unique()
genres_string = ', '.join(unique_genres)
# print('Genres: ' + genres_string)


# CLEAN CONSOLIDATED DATASET
# Sort and find duplicates
columns_to_check = ['title', 'release_year']
num_duplicates = df1.duplicated(subset=columns_to_check).sum()
# print("Number of duplicates:", num_duplicates)
df_sorted = df1.sort_values(by=['title', 'release_year'])
grouped = df_sorted.groupby(['title', 'release_year'])

# Merge duplicates
consolidation_rules = {
    'show_id': 'last',
    'platform': lambda x: ', '.join(x),
    'type': 'last',
    'director': 'last',
    'country': 'last',
    'cast': 'last',
    'date_added': 'last',
    'rating': 'last',
    'duration': 'last',
    'genre': lambda x: ', '.join(x),
    'description': 'last'}

df = grouped.agg(consolidation_rules).reset_index()

# Replace fields that have strings "nan" with a np.nan value
df.replace("nan", np.nan, inplace=True)

# Remove redundant values in the genre column using genre_mapping
for index, row in df.iterrows():
    genres = row['genre'].split(', ')
    new_genres = [genre_mapping[genre] if genre in genre_mapping else genre for genre in genres]
    df.at[index, 'genre'] = ', '.join(new_genres)
df['genre'] = df['genre'].apply(remove_duplicate_genres)

# Remove TV Shows from df
df = df[df['type'] == 'Movie']

# EXPORT DF TO CSV
# df.to_csv('movies_data.csv', index=False)
# print(df.sample(n=1))
# df.info()
