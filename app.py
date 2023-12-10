
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, request, session
import requests

app = Flask(__name__)


# Disabling cache,  note:  Flask didn't see the updates in JS and CSS files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ID = '######'
APP_SECRET = '######'
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

# to do 
url_variables = {
    'url_top_artists': 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=5&offset=5',
    'url_top_tracks': 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5&offset=5',
    'url_saved_tracks': 'https://api.spotify.com/v1/me/tracks?limit=5&offset=5',
    'url_recently_played': 'https://api.spotify.com/v1/me/player/recently-played?limit=10&offset=5',
    'url_current_user': 'https://api.spotify.com/v1/me',
    'url_top_genres': 'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=100&offset=0'
}


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

def get_genre_counts(data_top_genres):
    genre_list = [genre['genres'] for genre in data_top_genres['items']]
    genre_counts = {}

    for artist_genres in genre_list:
        for genre in artist_genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts

def get_top_n_genres(genre_counts, n=5):
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:n]
    return sorted_genres


# HOME PAGE
@app.route("/home")
def home():

    # Queries
    token = session["token"]
    header={"Content-Type":"application/json", "Authorization":f"Bearer {token}"}
    data_top_artists = requests.get(url_top_artists, headers=header).json()
    data_top_tracks = requests.get(url_top_tracks, headers=header).json()
    data_saved_tracks = requests.get(url_saved_tracks, headers=header).json()
    data_recently_played = requests.get(url_recently_played, headers=header).json()
    data_current_user = requests.get(url_current_user, headers=header).json()
    data_top_genres = requests.get(url_top_genres, headers=header).json()


    # Get the top 10 genres by occurrences
    genre_counts = get_genre_counts(data_top_genres)
    top_10_genres = get_top_n_genres(genre_counts)

    top1_artist_id = data_top_artists['items'][0]['id']
    top1_genre = data_top_genres['items'][0]['genres'][0]
    top1_genre_result = top1_genre.replace(' ', '+')

    url_recommendations = f'https://api.spotify.com/v1/recommendations?seed_artists={top1_artist_id}&seed_genres={top1_genre_result}&seed_tracks={top1_artist_id}'
    data_recommendations = requests.get(url_recommendations, headers=header).json()

    return render_template(
        "home.html",
        data_top_artists=data_top_artists,
        data_top_tracks=data_top_tracks,
        data_saved_tracks=data_saved_tracks,
        data_recently_played=data_recently_played,
        data_current_user=data_current_user,
        top_10_genres=top_10_genres,
        data_recommendations=data_recommendations
        )

@app.errorhandler(500)
def internal_server_error(e):
    return 'Spotify was unable to gather all the necessary information, make sure you have listening time before going to this site', 500


if __name__ == "__main__":
    app.run()
