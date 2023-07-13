from flask import Flask, request, jsonify
from src.model.order_model import orderGetItem
from src.plugins.producer import *


def init_app(app: Flask):
    @app.route("/order/create_item", methods=["POST"])
    def create_item():
        if request.method == "POST":
            data = request.get_json()
            produce_message("created", data)
        return jsonify({'message': 'Dado inserido com sucesso!'})


    @app.route("/order/update_item", methods=["PUT"])
    def update_item():
        if request.method == "PUT":
            data = request.get_json()
            produce_message("updated", data)
        return jsonify({'message': 'Dado atualizado com sucesso!'})


    @app.route("/order/delete_item", methods=["DELETE"])
    def delete_item():
        if request.method == "DELETE":
            data = request.get_json()
            produce_message("deleted", data)
        return jsonify({'message': 'Dado excluido com sucesso!'})


    @app.route("/order/get_item", methods=["GET"])
    def order_get_item():
        return orderGetItem()
