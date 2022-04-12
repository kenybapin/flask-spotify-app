# Create a flask app using spotify API


## Requirements
- python3
- requests
- flask


## Notes
- Authentification (token)
- What is callback URI ?
- Spotify API (top artists stats)


## Setup (local use)
1. git clone project
```
git clone
```
2. modify app.py with callback URI, client ID and secret
```
How to get Spotify callback URI, client ID and secret ?
https://support.heateor.com/get-spotify-client-id-client-secret/
```
3. launch app
``` 
python3 app.py
```
4. Access
```
http://127.0.0.1:5000/
```

# TO DO
1. Secure flask with HTTPS
2. Hosting your APP on cloud
2.1. HTTPS cerificate (cloudfare)
2.2. Cloud RUN (hebergement de l'application + nom de domaine + certificat https ???)


