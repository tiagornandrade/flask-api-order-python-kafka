from flask import Flask, request, jsonify 
import json


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def create_event():
    json_ = json.loads(request.data)
    with open('data.json', 'w') as f:
        json.dump(json_, f)
    return json_


@app.route("/test", methods=["GET","POST"])
def open_event():
    f = open('data.json')
    data = json.load(f)
    return data

if __name__ == "__main__":
    app.run(debug=True)