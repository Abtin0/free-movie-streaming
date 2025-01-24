from flask import Flask, render_template, request
import requests

app = Flask(__name__)

omdb_endpoint = "https://www.omdbapi.com/"
omdb_key = "afdfdee3"


def movie_request(user_input):
    response = requests.get(omdb_endpoint, params={"apikey": omdb_key, "s": user_input})
    response = response.json().get("Search", [])
    if response:
        return f'https://vidsrc.xyz/embed/movie/{response[0]["imdbID"]}'
    return None


def series_request(user_input):
    response = requests.get(omdb_endpoint, params={"apikey": omdb_key, "s": user_input})
    response = response.json().get("Search", [])
    if response:
        return f'https://vidsrc.xyz/embed/tv/{response[0]["imdbID"]}'
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie', methods=["GET", "POST"])
def movie():
    if request.method == "POST":
        user_input = request.form["user_input"]
        movie_endpoint = movie_request(user_input)
        if movie_endpoint:
            return render_template('movie.html', video_url=movie_endpoint)
        else:
            return render_template('movie.html', error="No movies found for your search.")
    return render_template('movie.html')


@app.route('/series', methods=["GET", "POST"])
def series():
    if request.method == "POST":
        user_input = request.form["user_input"]
        series_endpoint = series_request(user_input)
        if series_endpoint:
            return render_template('series.html', video_url=series_endpoint)
        else:
            return render_template('series.html', error="No series found for your search.")
    return render_template('series.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
