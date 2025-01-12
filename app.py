import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status()  # Will raise an exception for bad HTTP status codes
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return None


movie_data = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommendation System")

movie_titles = movie_data["title"].values
selected = st.selectbox("Select a movie", movie_titles)

def recommended_movies(movie):
    index = movie_data[movie_data["title"] == movie].index[0]

    # Sorting the movies by similarity score in descending order
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in distances:  # Get top 5 recommendations (excluding the selected movie)
        movie_id = movie_data.loc[i[0]].movie_id
        recommended_titles.append(movie_data.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_posters.append(poster if poster else "https://via.placeholder.com/150?text=No+Poster")

    return recommended_titles, recommended_posters

if st.button("Recommend me"):
    st.write(f"Recommended movies similar to **{selected}**:")
    titles, posters = recommended_movies(selected)

    # Dynamically display the movie recommendations
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(titles[i])
            st.image(posters[i], use_container_width=True)
