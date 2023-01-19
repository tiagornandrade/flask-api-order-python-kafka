import json
import requests
from tinydb import TinyDB
from uuid import uuid4
from flask import Flask, request, jsonify


app = Flask(__name__)

db = TinyDB('db.json')

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "order_details"

producer = KafkaProducer(retries=5, bootstrap_servers='localhost:9092')

@app.route("/create_item", methods=["POST"])
def create_item():
    if request.method == 'POST':
        content = request.get_json()
        # db.insert(content)

        future = producer.send(ORDER_KAFKA_TOPIC, json.dumps(content).encode("utf-8"))
        producer.flush()
        future.get(timeout=60)
    return jsonify(content) 

@app.route("/get_item", methods=["GET"])
def get_item():
    data = db.all()
    return data

if __name__ == "__main__":
    app.secret_key = "app2"
    app.run(debug=True)