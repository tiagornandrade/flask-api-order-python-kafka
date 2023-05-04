from flask import Flask, request, jsonify
from src.pub_sub.producer import producer_created, producer_deleted, producer_updated


app = Flask(__name__)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        data = request.get_json()
        producer_created(data)
        return jsonify({'message': 'Dado inserido com sucesso!'})

@app.route("/order/update_item", methods=["PUT"])
def update_item():
    if request.method == "PUT":
        data = request.get_json()
        producer_updated(data)
    return jsonify({'message': 'Dado atualizado com sucesso!'})


@app.route("/order/delete_item", methods=["DELETE"])
def delete_item():
    if request.method == "DELETE":
        data = request.get_json()
        producer_deleted(data)
    return jsonify({'message': 'Dado excluido com sucesso!'})


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_1"
    app.run(debug=True)
