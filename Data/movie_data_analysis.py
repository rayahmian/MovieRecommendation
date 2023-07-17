import pandas as pd
import numpy as np

# INITIALIZE THE DATA
adf = pd.read_csv('amazonprime_data.csv')
ddf = pd.read_csv('disneyplus_data.csv')
hdf = pd.read_csv('hulu_data.csv')
ndf = pd.read_csv('netflix_data.csv')

pd.set_option('display.max_rows', None)

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
df1 = df1[['show_id', 'platform', 'type', 'title', 'director', 'cast', 'country', 'date_added', 'release_year',
           'rating', 'duration', 'listed_in', 'description']]
# df1.info()

# Extract a string of countries movies were made in
df1['country'] = df1['country'].astype(str)
df_countries = df1['country'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
df_countries = df_countries.str.strip()
df_countries = df_countries[df_countries != '']
unique_countries = df_countries.unique()
countries_string = ', '.join(unique_countries)
# print('Countries :' + countries_string)

# Extract a string of the genres available
df1['listed_in'] = df1['listed_in'].astype(str)
df_genres = df1['listed_in'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)
df_genres = df_genres.str.strip()
unique_genres = df_genres.unique()
genres_string = ', '.join(unique_genres)
# print('Genres: ' + genres_string)

# MERGE DUPLICATES
# Count the number of duplicates
columns_to_check = ['title', 'release_year']
num_duplicates = df1.duplicated(subset=columns_to_check).sum()
print("Number of duplicates:", num_duplicates)

# Sort and find duplicates
df_sorted = df1.sort_values(by=['title', 'release_year'])
grouped = df_sorted.groupby(['title', 'release_year'])

consolidation_rules = {
    'show_id': 'last',
    'platform': lambda x: ', '.join(x),
    'type': 'last',
    'director': 'last',
    'cast': 'last',
    'date_added': 'last',
    'rating': 'last',
    'duration': 'last',
    'listed_in': lambda x: ', '.join(x),
    'description': 'last'}

df = grouped.agg(consolidation_rules).reset_index()

# Replace fields that have strings "nan" with a np.nan value
df.replace("nan", np.nan, inplace=True)
df.info()

# EXPORT
# Save the consolidated dataset to a CSV file
df.to_csv('movies_data.csv', index=False)
