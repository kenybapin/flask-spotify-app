from flask import Flask, render_template, redirect, request, make_response,session,redirect, jsonify
import requests

app = Flask(__name__)
# DIsabling cache,  note:  Flask didn't see the updates in JS and CSS files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ID = 'cc57db2e4e4d4f1ca09307a25f8a2e50'
APP_SECRET = 'a370ef230341461fafd93b612b0809f3'
app.secret_key = APP_SECRET

API_BASE = 'https://accounts.spotify.com'
REDIRECT_URI = "http://127.0.0.1:5000/api_callback"
SCOPE = 'user-top-read'
SHOW_DIALOG = False

# AUTH Step 1.
# the user logs in and authorizes access
@app.route("/")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={APP_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)

# MAIN APP
@app.route("/home")
def home():
    token = session["toke"]
    endpoint_url = "https://api.spotify.com/v1/me/top/artists?"
    limit=5
    time_range="long_term"
    offset=5
    query = f'{endpoint_url}time_range={time_range}&limit={limit}&offset={offset}'
    response = requests.get(query, headers={"Content-Type":"application/json", "Authorization":f"Bearer {token}"})
    data = response.json()
    return render_template("home.html.j2", data=data)

# AUTH Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
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
    session["toke"] = res_body.get("access_token")
    return redirect("home")

if __name__ == "__main__":
    app.run()