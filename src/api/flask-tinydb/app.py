from tinydb import TinyDB
from flask import Flask, request, jsonify


app = Flask(__name__)

db = TinyDB("db.json")


@app.route("/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        content = request.get_json()
        db.insert(content)
    return jsonify(content)


@app.route("/get_item", methods=["GET"])
def get_item():
    data = db.all()
    return data


if __name__ == "__main__":
    app.secret_key = "app_flask_tinydb"
    app.run(debug=True)
