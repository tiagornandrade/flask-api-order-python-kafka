import json
from flask import Flask, request, jsonify


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
def get_item():
    for message in consumer:
        consumed_message = message.value.decode("utf-8")
        return consumed_message


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka"
    app.run(debug=True)
