import streamlit as st
import json
from Classifier import KNearestNeighbours
from operator import itemgetter
import base64
import requests

def fetch_poster(movie_title):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('image.png')




# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)

def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table

if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    new_title = '<center style="font-family:sans-serif; color:Red; font-size: 42px;"><b>Movie Recommendation System</b></center>'
    st.markdown(new_title, unsafe_allow_html=True)
    apps = ['--Filter Movie Based on--', 'Movie based', 'Genres based'] 
    app_options = st.selectbox('', apps)
    
    if app_options == 'Movie based':
        st.markdown('',unsafe_allow_html=True)
        st.markdown('',unsafe_allow_html=True)
        st.markdown(f'<p style="color:Red;font-size:20px;">{"Select Movie name"}</p>', unsafe_allow_html=True)
        movie_select = st.selectbox('', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('')
        else:
            n = st.number_input('', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            st.markdown(f'<p style="color:Red;font-size:20px;">{"Number of Movies"}</p>', unsafe_allow_html=True)
            table = knn(test_point, n)
            st.markdown('',unsafe_allow_html=True)
            st.markdown('',unsafe_allow_html=True)
            st.markdown('',unsafe_allow_html=True)
            st.markdown(f'<p style="color:Red;font-size:20px;">{"Recommended Movies"}</p>',unsafe_allow_html=True)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
            print(table)
    elif app_options == apps[2]:
        options = st.multiselect('',genres)
        if options:
            imdb_score = st.slider('', 1, 10, 8)
            st.markdown(f'<p style="color:Red;font-size:20px;">{"IMDB Score"}</p>', unsafe_allow_html=True)
            st.markdown('',unsafe_allow_html=True)
            st.markdown('',unsafe_allow_html=True)
            n = st.number_input('', min_value=5, max_value=20, step=1)
            st.markdown(f'<p style="color:Red;font-size:20px;">{"Number of Movies"}</p>', unsafe_allow_html=True)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            st.markdown('',unsafe_allow_html=True)
            st.markdown('',unsafe_allow_html=True)
            st.markdown(f'<p style="color:Red;font-size:20px;">{"Recommended Movies"}</p>',unsafe_allow_html=True)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")

        else:
             
                st.markdown(f'<p style="color:Red;font-size:20px;">{"This is a simple Movie Recommender application. You can select the genres and change the IMDb score."}</p>', unsafe_allow_html=True)
    else:
        st.write('Select option')