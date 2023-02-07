from pub_sub.producer import producerCreated, producerDeleted
from flask import Flask, request, jsonify, redirect
from routes.order import orderGetItem


app = Flask(__name__)

@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        content = request.get_json()
        producerCreated(content)
    return jsonify(content)

@app.route("/order/delete_item", methods=["POST"])
def delete_item():
    if request.method == "POST":
        content = request.get_json()
        producerDeleted(content)
    return jsonify(content)

@app.route("/order/get_item", methods=["GET"])
def order_get_item():
    return orderGetItem()


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_order"
    app.run(debug=True, port=5001)
