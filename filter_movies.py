from tmdbv3api import TMDb, Discover
import streamlit as st

# TMDb API Setup
tmdb = TMDb()
tmdb.api_key = "244965477ee36ed344412138c664f50b"  # Your TMDb API Key
tmdb.language = "en"  # Set language to English
tmdb.debug = True  # Enable debug mode to troubleshoot issues

discover_api = Discover()

# Map genres to their TMDb IDs
genre_map = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "Thriller": 53,
    "War": 10752,
    "Western": 37,
}

# Map themes to keywords
theme_keywords = {
    "Magic": ["magic", "wizard", "spell"],
    "Futuristic": ["future", "space", "sci-fi", "technology"],
    "Animated": ["animated", "cartoon"],
    "Historical": ["history", "historical", "past"],
    "Action-packed": ["action", "explosion", "adventure"],
    "Romantic": ["romance", "love", "relationship"],
}

# Streamlit App Interface
st.title("Personalized Movie Recommendation Engine")

# Step 1: Select Genres
st.header("Step 1: Choose Your Favorite Genres")
available_genres = list(genre_map.keys())
selected_genres = st.multiselect("Select your favorite genres:", available_genres)

# Step 2: Select Themes
st.header("Step 2: Choose Your Interests/Themes")
themes = list(theme_keywords.keys())
selected_themes = st.multiselect("What themes do you enjoy in movies?", themes)

# Step 3: Fetch Movies and Filter
if selected_genres and selected_themes:
    st.header("Step 3: Movies Matching Your Interests")
    keywords = [keyword for theme in selected_themes for keyword in theme_keywords.get(theme, [])]

    genre_movies = []
    max_pages = 5  # Number of pages to fetch (adjust as needed)

    for genre in selected_genres:
        genre_id = genre_map.get(genre)
        if genre_id:
            for page in range(1, max_pages + 1):
                response = discover_api.discover_movies({"with_genres": genre_id, "release_date.gte": "2014-01-01", "page": page})
                if hasattr(response, "results"):
                    for movie in response.results:
                        if hasattr(movie, "overview") and any(keyword in movie.overview.lower() for keyword in keywords):
                            genre_movies.append(movie)
                else:
                    break  # Stop if no results for a page

    # Display Filtered Movies
    if genre_movies:
        user_responses = {}
        for movie in genre_movies[:20]:  # Show top 20 movies
            response = st.radio(
                f"Movie: {movie.title} (Release Date: {movie.release_date if hasattr(movie, 'release_date') else 'N/A'})",
                ["Watched", "Would like to watch", "Skip"],
                key=movie.id
            )
            user_responses[movie.title] = response

        # Generate Recommendations
        if st.button("Generate Recommendations"):
            liked_movies = [movie for movie, response in user_responses.items() if response == "Would like to watch"]
            if liked_movies:
                st.header("Movies Recommended for You:")
                for movie in liked_movies:
                    st.write(f"- {movie} (Based on your interests!)")
            else:
                st.error("Please mark at least one movie as 'Would like to watch' to get recommendations.")
    else:
        st.error("No movies found matching your selected genres and themes.")
else:
    st.warning("Please select at least one genre and one theme to see recommendations.")