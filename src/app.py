from kafka import KafkaProducer
from flask import Flask, request, jsonify
from utils.producer import producerCreated, producerDeleted, producerUpdated


app = Flask(__name__)

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        data = request.get_json()
        producerCreated(data)
        return jsonify({'message': 'Dado inserido com sucesso!'})

@app.route("/order/update_item", methods=["PUT"])
def update_item():
    if request.method == "PUT":
        data = request.get_json()
        producerUpdated(data)
    return jsonify({'message': 'Dado atualizado com sucesso!'})


@app.route("/order/delete_item", methods=["DELETE"])
def delete_item():
    if request.method == "DELETE":
        data = request.get_json()
        producerDeleted(data)
    return jsonify({'message': 'Dado excluido com sucesso!'})


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_1"
    app.run(debug=True)