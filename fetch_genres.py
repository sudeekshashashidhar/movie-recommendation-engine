from tmdbv3api import TMDb, Genre

# TMDb API Setup
tmdb = TMDb()
tmdb.api_key = "244965477ee36ed344412138c664f50b"  # Your API Key
tmdb.language = "en"

genre_api = Genre()

# Fetch all movie genres
movie_genres = genre_api.movie_list()
print("TMDb Movie Genres and IDs:")
for genre in movie_genres:
    print(f"{genre.name}: {genre.id}")