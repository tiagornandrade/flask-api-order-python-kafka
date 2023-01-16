from flask import Flask, request, jsonify 
import json
import os

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def create_event():
    # data = json.loads(request.data)
    data = request.json
    with open('data.json', 'w') as file:
        json.dump(data, file)
    return data


@app.route("/test", methods=["GET","POST"])
def open_event():
    with open("data.json") as file:
        data = json.load(file)

    return data

if __name__ == "__main__":
    app.run(debug=True)