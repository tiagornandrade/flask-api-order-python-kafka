import json
from producer import producerApi
from flask import Flask, request, jsonify
from routes.order.order import orderGetItem
from routes.transaction.transaction import transactionGetItem


app = Flask(__name__)

from kafka import KafkaProducer, KafkaConsumer

KAFKA_TOPIC = "order_details"

producer = KafkaProducer(
    retries=5, 
    bootstrap_servers="localhost:9092"
)
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    group_id="consumer-1",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        content = request.get_json()
        future = producer.send(KAFKA_TOPIC, json.dumps(content).encode("utf-8"))
        producer.flush()
        future.get(timeout=60)
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
