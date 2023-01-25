from kafkaProducerOrder import producerApi
from flask import Flask, request, jsonify
from routes.order.order import orderGetItem
from routes.transaction.transaction import transactionGetItem


app = Flask(__name__)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        content = request.get_json()
        producerApi(content)
    return jsonify(content)


@app.route("/order/get_item", methods=["GET"])
def order_get_item():
    return orderGetItem()


@app.route("/transaction/get_item", methods=["GET"])
def transaction_get_item():
    return transactionGetItem()


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka"
    app.run(debug=True)
