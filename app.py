import streamlit as st

import pickle

movie_data = pickle.load(open("movies_list.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

st.title("Movie Recommendation system")
# st.write("Hello, Streamlit!")

# age = st.selectbox(
#     "Age:",
#     ('>18','18','<18')
# )

# st.button('Validate')




movie_titles = movie_data["title"].values
selected = st.selectbox(
    "Select a movie",
    movie_titles
)




    
    
def recommended_movies(movie):
    index = movie_data[movie_data["title"] == movie].index[0]

    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x : x[1])
    moviess = []
    for i in distances[1 : 6]:
        print(movie_data.loc[i[0]]["title"])
        moviess.append(movie_data.loc[i[0]]["title"])
    return moviess
        


if st.button("Recommend me"):
    st.write(selected)
    listt = recommended_movies(selected)
    for i in listt:
        st.write(i)