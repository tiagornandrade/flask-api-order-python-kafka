# from pub_sub.producer import producerCreated
import json
import datetime
from uuid import uuid4
from kafka import KafkaProducer
from flask import Flask, request, jsonify
from database.dbConnect import connectionWrite


app = Flask(__name__)
connection = connectionWrite()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        data = request.get_json()

        user_id = str(uuid4())
        event_key = str(uuid4())
        name = data["name"]
        description = data["description"]
        price = data["price"]

        message = {
            "user_id": user_id,
            "event_key": event_key,
            "name": name,
            "description": description,
            "price": price,
        }
        producer_order.send(
            ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
        )
        return jsonify({'message': 'Dado inserido com sucesso!'})


@app.route("/order/update_item", methods=["PUT"])
def update_item():
    if request.method == "PUT":
        data = request.get_json()

        user_id = data["user_id"]
        event_key = str(uuid4())
        name = data["name"]
        description = data["description"]
        price = data["price"]

        message = {
            "user_id": user_id,
            "event_key": event_key,
            "name": name,
            "description": description,
            "price": price,
        }
        producer_order.send(
            ORDER_UPDATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
        )
    return jsonify({'message': 'Dado atualizado com sucesso!'})


@app.route("/order/delete_item", methods=["DELETE"])
def delete_item():
    if request.method == "DELETE":
        data = request.get_json()

        user_id = data["user_id"]
        event_key = str(uuid4())
        name = data["name"]
        description = data["description"]
        price = data["price"]

        message = {
            "user_id": user_id,
            "event_key": event_key,
            "name": name,
            "description": description,
            "price": price,
        }
        producer_order.send(
            ORDER_DELETED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
        )
    return jsonify({'message': 'Dado excluido com sucesso!'})


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_1"
    app.run(debug=True)
