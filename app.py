from flask import Flask, render_template, redirect, request, session
import requests

app = Flask(__name__)

# Disabling cache,  note:  Flask didn't see the updates in JS and CSS files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ID = '########################'
APP_SECRET = '#############################'
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
    
    top1_artist_id = data_top_artists['items'][0]['id']
    url_recommandations = f'https://api.spotify.com/v1/me/following?type=artist&after={top1_artist_id}&limit=10'
    data_recommandations = requests.get(url_recommandations, headers=header).json()

    return render_template(
        "home.html",
        data_top_artists=data_top_artists, 
        data_top_tracks=data_top_tracks,
        data_saved_tracks=data_saved_tracks, 
        data_recently_played=data_recently_played, 
        data_current_user=data_current_user, 
        data_recommandations=data_recommandations
        )

if __name__ == "__main__":
    app.run()