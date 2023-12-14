# Run a FLASK Web app using spotify API


Run a Flask web application and display some of your Spotify content :<br>
View your top tracks, artists and album. Check out your recently played tracks.

![image](preview.jpg?raw=true)

<br><br>
## Requirements
* **python3** with **requests** and **flask** librairies
```
$ pip3 install requests
$ pip3 install flask
```
* Create a Spotify account (sign up [here](www.spotify.com))
* Go to your [Dashboard page](https://developer.spotify.com/dashboard/login) and create an app.
  - Remember your **CLIENT ID** and **CLIENT SECRET**
  - Edit settings > add a Redirect URI with *http://127.0.0.1:5000/api_callback* <br>
    *loopback address for local use, 5000 is your default flask port*

<br><br>
## Notes related to user data

"By default, your application is set to 'developer mode,'<br>
In this mode, you can collect only your own data, and other users face restricted access, resulting in a 403 error.<br>

**How to allow other users to test your application ?**

a) On "developer mode", you need to add them via the Spotify [Dashboard](https://developer.spotify.com/dashboard/login) :<br> 
*App > Settings > User Management.*

b) To boost your application's visibility and bypass manual user addition, switch your application to "extended quota mode" :<br>
*App > Extension Request.* <br>
<br>
Following this, Spotify will examine and evaluate your application to ensure it aligns with their [Developer Policy](https://developer.spotify.com/policy).<br><br>

<br><br>
# Setup

1. git clone project
```
$ git clone https://github.com/kenybapin/flask-spotify-app/
```
2. Open **app.py** and according to your spotify app, edit the following values : 
   - APP_ID (CLIENT ID)
   - APP_SECRET (CLIENT SECRET)
   - REDIRECT_URI

# Run with python

``` 
$ python3 app.py

* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

    
# Run as container (docker)
1. Edit **app.py** and add os module
```
import os
```
2. Then, config your app with custom listening port and address
```
app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```
3. Finaly, build and run in a container 
```
docker build -t my-flask-app:latest .
docker run -it --rm -p 5000:5000 my-flask-app:latest
```


 
