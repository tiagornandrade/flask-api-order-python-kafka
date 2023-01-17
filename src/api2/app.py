from flask import Flask, request, jsonify 
import requests
import subprocess
import json
import os

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def create_event():
    if request.method == 'POST':
        content = request.get_json()
        pass1 = subprocess.call('python3 producer.py', shell=True)
        return jsonify(content) 


@app.route("/test", methods=["GET","POST"])
def open_event():
    response = requests.get('http://localhost:5000').text
    data = json.loads(response)
    return data

if __name__ == "__main__":
    app.run(debug=True)