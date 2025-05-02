import pickle
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('movie_recommender.log')
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Function to fetch poster using movie_id
def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=ID".format(movie_id)
        data = requests.get(url)
        data = data.json()
        
        # Check if poster_path exists
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            logger.info(f'Fetched poster for movie {movie_id}')
            return full_path
        else:
            logger.warning(f'No poster found for movie {movie_id}')
            return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image if no poster
    except Exception as e:
        logger.error(f'Error fetching poster for movie {movie_id}: {str(e)}')

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # Fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        
        logger.info(f'Recommended movies for {movie}: {recommended_movie_names}')
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        logger.error(f'Error recommending movies for {movie}: {str(e)}')

# Streamlit UI
st.header('Movie Recommender System')

# Load the models and movies data
try:
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))
    logger.info('Loaded movie list and similarity data')
except Exception as e:
    logger.error(f'Error loading movie list and similarity data: {str(e)}')

movie_list = movies['title'].values

# Dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendation when button is clicked
if st.button('Show Recommendation'):
    try:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        # Display recommended movies in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
        logger.info('Displayed recommended movies')
    except Exception as e:
        logger.error(f'Error displaying recommended movies: {str(e)}')import streamlit as st
import requests

# Function to fetch poster using movie_id
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ID".format(movie_id)
    data = requests.get(url)
    data = data.json()
    
    # Check if poster_path exists
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image if no poster

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.header('Movie Recommender System')

# Load the models and movies data
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values

# Dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendation when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommended movies in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
