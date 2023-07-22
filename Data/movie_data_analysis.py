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

# Rename the "listed_in" column to "genre"
df1.rename(columns={'listed_in': 'genre'}, inplace=True)
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
print('Genres: ' + genres_string)


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

# Remove redundant values in the genre column
genre_mapping = {
    "International": ["International", "International TV Shows", "International Movies"],
    "Spanish": ["Spanish-Language TV Shows", "Latino"],
    "British": ["British TV Shows"],
    "Korean": ["Korean TV Shows"],
    "Children & Family": ["Kids", "Children & Family Movies", "Kids' TV", "Family"],
    "Animation": ["Animation", "Adult Animation", "Cartoons"],
    "Documentary": ["Documentary", "Docuseries", "Documentaries"],
    "Science & Nature": ["Animals & Nature", "Science & Nature TV", "Science & Technology", "Special Interest"],
    "Anime": ["Anime", "Anime Features", "Anime Series"],
    "Sports": ["Sports", "Sports Movies"],
    "Teen & Young Adult": ["Teen TV Shows", "Young Adult Audience", "Coming of Age", "Teen"],
    "History": ["History", "Historical"],
    "Action & Adventure": ["Action", "Action-Adventure", "TV Action & Adventure", "Action & Adventure", "Adventure",
                           "Survival"],
    "Horror": ["TV Horror", "Horror", "Horror Movies"],
    "Science Fiction & Fantasy": ["Science Fiction", "TV Sci-Fi & Fantasy", "Fantasy", "Sci-Fi & Fantasy"],
    "Mystery": ["Mystery", "TV Mysteries"],
    "Romantic": ["Romance", "Romantic Movies", "Romantic TV Shows"],
    "Crime": ["Crime TV Shows", "Crime"],
    "Drama": ["TV Dramas", "Dramas", "Drama", "Soap Opera / Melodrama"],
    "Musicals": ["Musical", "Music & Musicals"],
    "Thriller": ["Thriller", "Thrillers", "TV Thrillers", "Suspense"],
    "Classic & Cult": ["Classic & Cult TV", "Classic Movies", "Cult Movies", "Classics"],
    "Arts & Lifestyle": ["Arts, Entertainment, and Culture", "Concert Film", "Music Videos and Concerts",
                         "Lifestyle & Culture", "Lifestyle", "Music", "Dance", "Travel"],
    "Faith & Spirituality": ["Faith & Spirituality", "Faith and Spirituality"],
    "LGBTQ+": ["LGBTQ", "LGBTQ+", "LGBTQ Movies"],
    "Health & Wellness": ["Fitness", "Health & Wellness"],
    "Game Show": ['Game Show / Competition', "Game Shows"],
    "Reality TV": ["Reality TV", "Unscripted", "Reality"],
    "Talk Show & Variety": ["Show and Variety", "Talk Show and Variety", "Talk Show", "Variety", "Late Night"],
    "Comedy": ["Comedy", "Parody", "TV Comedies", "Sitcom"],
    "Stand-Up": ["Stand-Up Comedy & Talk Shows", "Stand Up", "Sketch Comedy", "Stand-Up Comedy"]
}

df['genre'] = df['genre'].apply(map_genres)
# print(df.loc[15283, 'genre'])
