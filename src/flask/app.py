import os
import json
import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, request, jsonify


app = Flask(__name__)

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect('postgresql://localhost/market_db')

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
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""SELECT * FROM items_by_id;""")
            get_itens = cursor.fetchall()
            cursor.close()
            response_itens = [row_to_dict(x) for x in get_itens]
    return response_itens

def row_to_dict(row):
    return dict({
        'id': row['id'],
        'name': row['name'],
        'description': row['description'],
        'price': row['price']
    })


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka"
    app.run(debug=True)
