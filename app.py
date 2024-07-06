from flask import Flask, jsonify, request, render_template_string
import googlemaps
from googlemaps import Client
import json
import requests

app = Flask(__name__)

@app.route("/home")
def showing_movies(): #function for displaying all the available shown movies 
    
    apikey = "xxxxxxxxxxxxxx" 
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={apikey}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZDgyMDRlZjYwNDdiMGJmNWRhNGEwMjBjYjM0NTc2ZCIsInN1YiI6IjY2MmJkOTIwNmUwZDcyMDExZTFmYzc3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dr766GCo0jnuJ1zw62-im0MOLM26gMOogdfni0ljsIs"
    }

    response = requests.get(url, headers=headers)
    movie_data = response.json()
    movies = movie_data['results']

    movie_links = [f'<a href="/movies/{movie["id"]}">{movie["title"]}</a>' for movie in movies]
    return "<br>".join(movie_links)

def nearby_cinemas(): #function for displaying all the available cinemas nearby if i can get this piece of shit API to work properly
   return None

@app.route("/movies/<int:movie_id>")
def movie_details(movie_id):
    apikey = "xxxxxxxxxxxxxx" 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apikey}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZDgyMDRlZjYwNDdiMGJmNWRhNGEwMjBjYjM0NTc2ZCIsInN1YiI6IjY2MmJkOTIwNmUwZDcyMDExZTFmYzc3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dr766GCo0jnuJ1zw62-im0MOLM26gMOogdfni0ljsIs"
    }

    response = requests.get(url, headers=headers)
    movie_data = response.json()

    movie_title = movie_data['title']
    movie_overview = movie_data['overview']

    return render_template_string(
        "<h1>{{ title }}</h1><p>{{ overview }}</p>",
        title=movie_title,
        overview=movie_overview
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
