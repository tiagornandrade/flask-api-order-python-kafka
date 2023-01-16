from flask import Flask, request, jsonify 


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def create_event():
    return jsonify(request.json)


if __name__ == "__main__":
    app.run(debug=True)