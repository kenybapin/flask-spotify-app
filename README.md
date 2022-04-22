# Run a FLASK Web app using spotify API


Run a Flask web application and display some of your Spotify.<br>
View your top tracks, artists and album. Check out your recently played tracks.

![image](preview.jpg?raw=true)

<br>

source: [https://kbapin.pythonanywhere.com/](https://kbapin.pythonanywhere.com/)
## Requirements
* Install **python3** with **requests** and **flask** librairies
* Create a Spotify acount (sign up [here](www.spotify.com))
* Go to your [Dashboard page](https://developer.spotify.com/dashboard/login) and create an app.
  - Please note your own **CLIENT ID** and **CLIENT SECRET**
  - Edit settings > add a Redirect URI with *http://127.0.0.1:5000/api_callback* (for local use, 5000 is the default flask port)
 

## Setup
1. git clone project
```
$ git clone https://github.com/kenybapin/flask-spotify-app/
```
2. Open **app.py** and according to your spotify app, edit these variables values : 
   - APP_ID (CLIENT ID)
   - APP_SECRET (CLIENT SECRET)
   - REDIRECT_URI

4. Run the Web Application
``` 
$ python3 app.py

* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Known issues
- Get an Unhandled error when user token is expired after 1 hour session.
*Access tokens issued from the Spotify account service has a lifetime of one hour.*

Workaround: Refresh your webpage or restart Flask app.
