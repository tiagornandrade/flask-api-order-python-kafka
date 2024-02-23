from pub_sub.producer import producerCreated
from flask import Flask, request, jsonify, redirect


app = Flask(__name__)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    return redirect("http://localhost:5001/order/create_item")


@app.route("/order/update_item", methods=["POST"])
def update_item():
    if request.method == "POST":
        content = request.get_json()
        producerCreated(content)
    return jsonify(content)


@app.route("/order/delete_item", methods=["POST"])
def delete_item():
    return redirect("http://localhost:5001/order/delete_item")


@app.route("/order/get_item", methods=["GET"])
def order_get_item():
    return redirect("http://localhost:5001/order/get_item")


@app.route("/transaction/get_item", methods=["GET"])
def transaction_get_item():
    return redirect("http://localhost:5002/transaction/get_item")


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka"
    app.run(debug=True)
