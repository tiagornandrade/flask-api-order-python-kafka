from pub_sub.producer import producerCreated, producerDeleted
from database.dbConnect import connectionWrite
from flask import Flask, request, jsonify, redirect
from routes.order import orderGetItem
from uuid import uuid4


app = Flask(__name__)
connection = connectionWrite()

@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        content = request.get_json()
        data = content
        id = str(uuid4())
        name = data["name"]
        description = data["description"]
        price = data["price"]

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO public.order (id, name, description, price) VALUES (%s,%s,%s,%s) RETURNING id;""",
                (id, name, description, price),
            )
            connection.commit()
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

# @app.route("/order/update_item", methods=["PUT"])
# def order_update_item():
#     return orderUpdateItem()


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_write"
    app.run(debug=True, port=5001)
