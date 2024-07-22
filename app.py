from flask import Flask, jsonify, request, render_template_string, Response
import json
#from nearby_cinema import nearby_cinemas

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

@app.route('/nearby', methods=['GET', 'POST'])
def nearby() -> str:
    if request.method == 'POST':
        location = request.form['location']
        radius = request.form['radius']
        keyword = "cinemas"
        api_key = "AIzaSyA0P_Dh5HXIko4fF-k0Y9QZEI3yGuWAqFQ"  # Replace with your actual API key

        base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": location,
            "radius": radius,
            "keyword": keyword,
            "key": api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            places = [f"{result['name']}, {result.get('vicinity', 'No address available')}" for result in data["results"]]
        else:
            places = [f"Error: {data.get('status')}, {data.get('error_message')}"]

        return render_template_string(TEMPLATE, places=places)
    return render_template_string(TEMPLATE)

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>Nearby Places Finder</title>
  </head>
  <body>
    <h1>Cinemas near you</h1>
    <form method="post" action="/nearby">
      <label for="location">Location (latitude,longitude):</label><br>
      <input type="text" id="location" name="location" required><br><br>
      <label for="radius">Radius (meters):</label><br>
      <input type="number" id="radius" name="radius" required><br><br>
      <label for="keyword">Keyword:</label><br>
      <input type="text" id="keyword" name="keyword" required><br><br>
      <input type="submit" value="Find">
    </form>

    {% if places %}
      <h2>Results:</h2>
      <ul>
        {% for place in places %}
          <li>{{ place }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  </body>
</html>
"""
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
