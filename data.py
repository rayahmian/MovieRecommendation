from mapping import genre_mapping, rating_mapping, rating_mapping2
import pandas as pd
import numpy as np
import os


def remove_duplicate_genres(genre_string):
    g = genre_string.split(', ')
    ug = sorted(set(g), key=g.index)
    return ', '.join(ug)


# INITIALIZE THE DATA
# Read files
file_pathA = os.path.join(os.path.dirname(__file__), 'amazonprime_data.csv')
file_pathD = os.path.join(os.path.dirname(__file__), 'disneyplus_data.csv')
file_pathH = os.path.join(os.path.dirname(__file__), 'hulu_data.csv')
file_pathN = os.path.join(os.path.dirname(__file__), 'netflix_data.csv')

adf = pd.read_csv(file_pathA)
ddf = pd.read_csv(file_pathD)
hdf = pd.read_csv(file_pathH)
ndf = pd.read_csv(file_pathN)

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

# Merge all the data
df1 = pd.concat([adf, ddf, hdf, ndf], ignore_index=True)
# df1.info()


# CLEAN DATA
# Merge Duplicates
columns_to_check = ['title', 'release_year']
num_duplicates = df1.duplicated(subset=columns_to_check).sum()
df_sorted = df1.sort_values(by=['title', 'release_year'])
grouped = df_sorted.groupby(['title', 'release_year'])
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
    'listed_in': lambda x: ', '.join(x),
    'description': 'last'}
df = grouped.agg(consolidation_rules).reset_index()

# Replace fields that have strings "nan" with a np.nan value
df.replace("nan", np.nan, inplace=True)

# Remove TV Shows from df
df = df[df['type'] == 'Movie']

# Rename the listed_in column to genre
df.rename(columns={'listed_in': 'genre'}, inplace=True)

# Reorganize the columns
column_order = ['title', 'show_id', 'type', 'platform', 'director', 'cast', 'country', 'date_added', 'release_year',
                'rating', 'duration', 'genre', 'description']
df = df.reindex(columns=column_order)

# Only keep entries that have duration in minutes
df['duration'] = df['duration'].astype(str)
df = df[~df['duration'].str.contains('Season')]
df['duration'] = df['duration'].str.extract('(\d+)').astype(float)

# Format the ratings
df['rating'] = df['rating'].astype(str)
df = df[~df['rating'].str.contains('Season')]
df['rating'] = df['rating'].replace(rating_mapping, regex=True)
df['rating'] = df['rating'].replace(rating_mapping2)

# Format genres
for index, row in df.iterrows():
    genres = row['genre'].split(', ')
    new_genres = [genre_mapping[genre] if genre in genre_mapping else genre for genre in genres]
    df.at[index, 'genre'] = ', '.join(new_genres)
df['genre'] = df['genre'].apply(remove_duplicate_genres)

# EXPORT DF TO CSV
# df.to_csv('movies_data.csv', index=False)
# print(df.sample(n=1))
# df.info()
