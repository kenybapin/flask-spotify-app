from flask import Flask, render_template, redirect, request, session, url_for, abort
import requests
from requests.exceptions import RequestException, HTTPError

app = Flask(__name__)


# Disabling cache,  note:  Flask didn't see the updates in JS and CSS files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ID = '####'
APP_SECRET = '#####'
app.secret_key = APP_SECRET

API_BASE = 'https://accounts.spotify.com'
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"
SCOPE = 'user-top-read,user-library-read,user-read-recently-played,user-read-private,user-read-email,user-follow-read'
SHOW_DIALOG = True

# URLs
url_top_artists = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=5&offset=5'
url_top_tracks = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5&offset=5'
url_saved_tracks = 'https://api.spotify.com/v1/me/tracks?limit=5&offset=5'
url_recently_played = 'https://api.spotify.com/v1/me/player/recently-played?limit=10&offset=5'
url_current_user = 'https://api.spotify.com/v1/me'
url_top_genres = 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=100&offset=0'


# AUTH Step 1: log in and Request for User Authorization
@app.route("/")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={APP_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)

# AUTH Step 2: Request Spotify and access tokens;
@app.route("/api_callback")
def api_callback():

    session.clear()
    code = request.args.get('code')
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:5000/api_callback",
        "client_id":APP_ID,
        "client_secret":APP_SECRET
        })
    res_body = res.json()
    print(res.json())
    session["token"] = res_body.get("access_token")
    return redirect("home")




## RETRIEVE DATA

def fetch_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        if http_err.response.status_code == 403:
            # Redirect to the forbidden_error handler
            abort(403)
        else:
            print(f"HTTP error ({http_err.response.status_code}) when fetching data from {url}: {http_err}")
            return None
    except RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


# Get the top5 genres
def get_genres(data_top_genres, n=5):
    if data_top_genres is None:
        print("Error: data_top_genres is None")
        return {}, []

    genre_list = [genre['genres'] for genre in data_top_genres.get('items', [])]
    genre_counts = {}

    for artist_genres in genre_list:
        for genre in artist_genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    if not genre_counts or len(genre_counts) == 0:
        print("Error: genre_counts is empty")
        return {}, []

    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return genre_counts, sorted_genres


# Capture the top1 genre and artist to use them in the recommendations URL.  
def capture_top_genre_and_artist(data_top_artists, data_top_genres):
    try:
        top1_artist_id = data_top_artists['items'][0]['id']
        genre_counts, _ = get_genres(data_top_genres, n=1)
        top1_genre_result = list(genre_counts.keys())[0].replace(' ', '+')

        if top1_artist_id is None or top1_genre_result is None:
            raise ValueError("Top 1 artist ID or genre result is None")

        return top1_artist_id, top1_genre_result

    except (IndexError, KeyError, TypeError) as e:
        # Handle the exception based on your requirements
        print(f"Error in capture_top_genre_and_artist: {e}")
        return None, None


# HOME PAGE
@app.route("/home")
def home():

    # Queries
    token = session["token"]
    header={"Content-Type":"application/json", "Authorization":f"Bearer {token}"}
    
    # Check if all requests are valid
    data_top_artists = fetch_data(url_top_artists, header)
    data_top_tracks = fetch_data(url_top_tracks, header)
    data_saved_tracks = fetch_data(url_saved_tracks, header)
    data_recently_played = fetch_data(url_recently_played, header)
    data_current_user = fetch_data(url_current_user, header)
    data_top_genres = fetch_data(url_top_genres, header)

    # get_top5_genres
    genre_counts, sorted_genres = get_genres(data_top_genres)
    top_5_genres =  sorted_genres

    # capture_top_genre_and_artist
    top1_artist_id, top1_genre_result = capture_top_genre_and_artist(data_top_artists, data_top_genres)
    
    # fetch recommendations
    url_recommendations = f'https://api.spotify.com/v1/recommendations?seed_artists={top1_artist_id}&seed_genres={top1_genre_result}&seed_tracks={top1_artist_id}'
    data_recommendations = fetch_data(url_recommendations, header)

    # Check if any data is None and redirect to the error handler
    if data_top_artists is None or data_top_tracks is None or data_recently_played is None:
        abort(403)

    return render_template(
        "home.html",
        data_top_artists=data_top_artists,
        data_top_tracks=data_top_tracks,
        data_saved_tracks=data_saved_tracks,
        data_recently_played=data_recently_played,
        data_current_user=data_current_user,
        top_5_genres=top_5_genres,
        data_recommendations=data_recommendations
        )

# favicon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.ico')

@app.errorhandler(500)
def internal_server_error(e):
    return 'Internal Error', 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

if __name__ == "__main__":
    app.run()
