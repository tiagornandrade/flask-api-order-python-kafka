from flask import Flask, request, jsonify 
import requests
import subprocess
import json
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def create_event():
    with open('backend.json', 'a') as f:
        json_ = json.loads(request.data)
        json.dump(json_, f)
    return json_

@app.route("/test", methods=["GET","POST"])
def open_event():
    response = requests.get('http://localhost:5000').text
    data = json.loads(response)
    return data

if __name__ == "__main__":
    app.run(debug=True)