import os
from flask import Flask, render_template, redirect,redirect, jsonify, json
import requests


app = Flask(__name__)
# DIsabling cache,  note:  Flask didn't see the updates in JS and CSS files
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True
FLASK_ENV= "development"
DEBUG=True

@app.route("/")
def home():
    filename = os.path.join(app.static_folder, 'data', 'sample.json')
    with open(filename) as test_file:
        data = json.load(test_file)
    return render_template("home.html.j2", data=data)

if __name__ == "__main__":
    app.run()