from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

omdb_endpoint = "https://www.omdbapi.com/"
omdb_key = "afdfdee3"
# Load the endpoints from the JSON file
with open("static/endpoint.json", "r") as f:
    data = f.read()
    endpoints = json.loads(data)


def movie_request(user_input, endpoint_key):
    # Get the endpoint URL for the selected endpoint_key
    selected_endpoint = request.form["endpoint"]

    # Make the request to the selected endpoint
    response = requests.get(omdb_endpoint, params={"apikey": omdb_key, "s": user_input})

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if data.get("Search"):
            imdb_id = data["Search"][0]["imdbID"]
            poster = data["Search"][0]["Poster"]
            movie_name = data["Search"][0]["Title"]
            embed_url = f"{selected_endpoint}/movie/{imdb_id}"
            return embed_url, poster, movie_name
    return None


def series_request(user_input, endpoint_key):
    selected_endpoint = request.form["endpoint"]

    # Make the request to the selected endpoint
    response = requests.get(omdb_endpoint, params={"apikey": omdb_key, "s": user_input})

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        if data.get("Search"):
            imdb_id = data["Search"][0]["imdbID"]
            embed_url = f"{selected_endpoint}/tv/{imdb_id}"
            return embed_url
    return None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie', methods=["GET", "POST"])
def movie():
    if request.method == "POST":
        user_input = request.form["user_input"]
        endpoint_key = request.form["endpoint"]

        # Call the movie_request function
        movie_endpoint, poster, name = movie_request(user_input, endpoint_key)

        # Return the result based on whether a video URL is found
        if movie_endpoint:
            return render_template('movie.html', video_url=movie_endpoint, endpoints=endpoints,  poster=poster, name=name)
        else:
            return render_template('movie.html', error="No movies found for your search.", endpoints=endpoints)

    # Initial GET request, render the movie page with available endpoints
    return render_template('movie.html', endpoints=endpoints)


@app.route('/series', methods=["GET", "POST"])
def series():
    if request.method == "POST":
        user_input = request.form["user_input"]
        endpoint_key = request.form["endpoint"]

        # Call the series_request function
        series_endpoint = series_request(user_input, endpoint_key)

        # Return the result based on whether a video URL is found
        if series_endpoint:
            return render_template('series.html', video_url=series_endpoint, endpoints=endpoints)
        else:
            return render_template('series.html', error="No series found for your search.", endpoints=endpoints)

    # Initial GET request, render the series page with available endpoints
    return render_template('series.html', endpoints=endpoints)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
