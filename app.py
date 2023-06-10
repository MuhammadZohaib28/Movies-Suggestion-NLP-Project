from flask import Flask, request, render_template
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('Model/movies_list.pkl', 'rb'))
similarity = pickle.load(open('Model/similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/?api_key=e3294479c3aee3747aa7fd6aad8992be&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_suggestion(movie):
    
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies_name = []
        recommended_movies_poster = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movieId
            recommended_movies_poster.append(fetch_poster(movie_id))
            recommended_movies_name.append(movies.iloc[i[0]].title)
        return recommended_movies_name, recommended_movies_poster

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/suggestion', methods=['GET', 'POST'])
def suggestion():
    movie_list = movies['title'].values
    status = False

    if request.method == 'POST':
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommended_movies_name, recommended_movies_poster = get_suggestion(movies_name)  # Updated function name
                print(recommended_movies_name)
                status = True
                return render_template("suggestion.html", movies_name=recommended_movies_name, poster=recommended_movies_poster, movie_list=movie_list, statuss = status)
        except Exception as e:
            error = {'error': e}
            return render_template("suggestion.html", error=error, movie_list=movie_list, statuss = status)
    else:
        return render_template("suggestion.html", movie_list=movie_list, statuss=status)


if __name__ == '__main__':
    app.debug = True
    app.run()
