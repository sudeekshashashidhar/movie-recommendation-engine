from tmdbv3api import TMDb, Discover
import streamlit as st

# TMDb API Setup
tmdb = TMDb()
tmdb.api_key = "244965477ee36ed344412138c664f50b"  # Your TMDb API Key
tmdb.language = "en"  # Set language to English
tmdb.debug = True  # Enable debug mode to troubleshoot issues

discover_api = Discover()  # Use the Discover class for discovering movies

# Streamlit App Interface
st.title("Personalized Movie Recommendation Engine")

# Step 1: Select Genres
st.header("Step 1: Choose Your Favorite Genres")
available_genres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "Thriller", "War", "Western"
]
selected_genres = st.multiselect("Select your favorite genres:", available_genres)

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

# Step 2: Select Themes
st.header("Step 2: Choose Your Interests/Themes")
themes = ["Magic", "Futuristic", "Animated", "Historical", "Action-packed", "Romantic"]
selected_themes = st.multiselect("What themes do you enjoy in movies?", themes)

# Step 3: Fetch Movies Based on Selected Genres
if selected_genres:
    st.header("Step 3: Movies Matching Your Interests")
    genre_movies = []

    for genre in selected_genres:
        genre_id = genre_map.get(genre)
        if genre_id:
            # Fetch movies for the genre
            response = discover_api.discover_movies({"with_genres": genre_id, "release_date.gte": "2014-01-01"})

            # Ensure the response is iterable and extract relevant data
            if hasattr(response, "results"):  # Check if 'results' exists
                movies = response.results
                genre_movies.extend(list(movies)[:10])  # Convert to list and limit to top 10
            else:
                st.error(f"Unexpected response format for genre: {genre}")
                st.write(response)

    # Display Movies and Let Users Interact
    user_responses = {}
    for movie in genre_movies[:10]:  # Show top 10 movies overall
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
                st.write(f"- {movie} (Recommended based on your interest!)")
        else:
            st.error("Please mark at least one movie as 'Would like to watch' to get recommendations.")