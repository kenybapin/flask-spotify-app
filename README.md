# FLASK Web app using spotify API


[https://kbapin.pythonanywhere.com/](https://kbapin.pythonanywhere.com/)
<br>
 ![alt text](https://github.com/kenybapin/flask-spotify-app/blob/main/preview.jpg?raw=true)

## Requirements
* Install **python3** with **requests** and **flask** librairies
* Create a Spotify acount (sign up [here](www.spotify.com))
* Go to your [Dashboard page](https://developer.spotify.com/dashboard/login) and create an app.
  - Please note **CLIENT ID** and **CLIENT SECRET**
  - Edit settings > add a Redirect URI with *http://127.0.0.1:5000/api_callback* (for local use, 5000 is the default flask port)
 

## Setup
1. git clone
```
$ git clone https://github.com/kenybapin/flask-spotify-app/
```
2. Open **app.py** and changes theses values according to your spotify app:
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
- Token expiration error after 1 hour.<br>
*Access tokens issued from the Spotify account service has a lifetime of one hour.*

Workaround: Refresh your webpage or restart Flask app.
