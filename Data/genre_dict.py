# Create a dictionary of acceptable genres
genre_mapping = {
    'Action': 'Action & Adventure',
    'Action-Adventure': 'Action & Adventure',
    'TV Action & Adventure': 'Action & Adventure',
    'Action & Adventure': 'Action & Adventure',
    'Adventure': 'Action & Adventure',
    'Survival': 'Action & Adventure',
    'Animation': 'Animation',
    'Adult Animation': 'Animation',
    'Cartoons': 'Animation',
    'Anime': 'Anime',
    'Anime Features': 'Anime',
    'Anime Series': 'Anime',
    'Arts, Entertainment, and Culture': 'Arts & Lifestyle',
    'Concert Film': 'Arts & Lifestyle',
    'Music Videos and Concerts': 'Arts & Lifestyle',
    'Lifestyle & Culture': 'Arts & Lifestyle',
    'Lifestyle': 'Arts & Lifestyle',
    'Music': 'Arts & Lifestyle',
    'Dance': 'Arts & Lifestyle',
    'Travel': 'Arts & Lifestyle',
    'British TV Shows': 'British',
    'Kids': 'Children & Family',
    'Children & Family Movies': 'Children & Family',
    "Kids' TV": 'Children & Family',
    'Family': 'Children & Family',
    'Classic & Cult TV': 'Classic & Cult',
    'Classic Movies': 'Classic & Cult',
    'Cult Movies': 'Classic & Cult',
    'Classics': 'Classic & Cult',
    'Comedy': 'Comedy',
    'Parody': 'Comedy',
    'TV Comedies': 'Comedy',
    'Sitcom': 'Comedy',
    'Crime TV Shows': 'Crime',
    'Crime': 'Crime',
    'Documentary': 'Documentary',
    'Docuseries': 'Documentary',
    'Documentaries': 'Documentary',
    'TV Dramas': 'Drama',
    'Dramas': 'Drama',
    'Drama': 'Drama',
    'Soap Opera / Melodrama': 'Drama',
    'Faith & Spirituality': 'Faith & Spirituality',
    'Faith and Spirituality': 'Faith & Spirituality',
    'Game Show / Competition': 'Game Show',
    'Game Shows': 'Game Show',
    'Fitness': 'Health & Wellness',
    'Health & Wellness': 'Health & Wellness',
    'History': 'History',
    'Historical': 'History',
    'TV Horror': 'Horror',
    'Horror': 'Horror',
    'Horror Movies': 'Horror',
    'International': 'International',
    'International TV Shows': 'International',
    'International Movies': 'International',
    'Korean TV Shows': 'Korean',
    'LGBTQ': 'LGBTQ+',
    'LGBTQ+': 'LGBTQ+',
    'LGBTQ Movies': 'LGBTQ+',
    'Musical': 'Musicals',
    'Music & Musicals': 'Musicals',
    'Mystery': 'Mystery',
    'TV Mysteries': 'Mystery',
    'Reality TV': 'Reality TV',
    'Unscripted': 'Reality TV',
    'Reality': 'Reality TV',
    'Romance': 'Romantic',
    'Romantic Movies': 'Romantic',
    'Romantic TV Shows': 'Romantic',
    'Animals & Nature': 'Science & Nature',
    'Science & Nature TV': 'Science & Nature',
    'Science & Technology': 'Science & Nature',
    'Special Interest': 'Science & Nature',
    'Science Fiction': 'Science Fiction & Fantasy',
    'TV Sci-Fi & Fantasy': 'Science Fiction & Fantasy',
    'Fantasy': 'Science Fiction & Fantasy',
    'Sci-Fi & Fantasy': 'Science Fiction & Fantasy',
    'Spanish-Language TV Shows': 'Spanish',
    'Latino': 'Spanish',
    'Sports': 'Sports',
    'Sports Movies': 'Sports',
    'Stand-Up Comedy & Talk Shows': 'Stand-Up',
    'Stand Up': 'Stand-Up',
    'Sketch Comedy': 'Stand-Up',
    'Stand-Up Comedy': 'Stand-Up',
    'Show and Variety': 'Talk Show & Variety',
    'Talk Show and Variety': 'Talk Show & Variety',
    'Talk Show': 'Talk Show & Variety',
    'Variety': 'Talk Show & Variety',
    'Late Night': 'Talk Show & Variety',
    'Teen TV Shows': 'Teen & Young Adult',
    'Young Adult Audience': 'Teen & Young Adult',
    'Coming of Age': 'Teen & Young Adult',
    'Teen': 'Teen & Young Adult',
    'Thriller': 'Thriller',
    'Thrillers': 'Thriller',
    'TV Thrillers': 'Thriller',
    'Suspense': 'Thriller'}