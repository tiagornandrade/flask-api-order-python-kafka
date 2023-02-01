from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import requests
import json


app = Flask(__name__)

db = TinyDB('backend.json')

@app.route("/", methods=["GET", "POST"])
def create_event():
    if request.method == "POST":
        content = db.insert(request.get_json())
        return jsonify(content)


@app.route("/test", methods=["GET", "POST"])
def open_event():
    #response = requests.get("http://localhost:5000").text
    #data = json.loads(response)
    #return data
    return json.load(db.all())

    #with open('backend.json') as f:
    #    feeds = json.load(f)
    #    n = [a for a in feeds]
    #    return jsonify(n)


if __name__ == "__main__":
    app.run(debug=True)
