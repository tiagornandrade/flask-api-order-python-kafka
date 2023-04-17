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
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)


@app.route("/order/create_item", methods=["POST"])
def create_item():
    if request.method == "POST":
        data = request.get_json()
        id = str(uuid4())
        name = data["name"]
        description = data["description"]
        price = data["price"]
        created_at = datetime.datetime.now()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO public.order (id, name, description, price, created_at) VALUES (%s,%s,%s,%s,%s) RETURNING id;",
                (id, name, description, price, created_at),
            )
            connection.commit()

        message = {
            "id": id,
            "name": name,
            "description": description,
            "price": price,
        }
        producer_order.send(
            ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
        )
        return jsonify({'message': 'Dados inseridos com sucesso!'})


@app.route("/order/update_item/<string:id>", methods=["POST"])
def update_item(id):
    data = request.json
    name = data["name"]
    description = data["description"]
    price = data["price"]
    updated_at = datetime.datetime.now()

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE public.order SET name = %s, description = %s, price = %s, updated_at = %s WHERE id = %s;",
            (name, description, price, updated_at, id),
        )
        connection.commit()

    message = {
        "id": id,
        "name": name,
        "description": description,
        "price": price,
        "updated_at": updated_at
    }
    producer_order.send(
        ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    return jsonify({'message': 'Dados atualizados com sucesso!'})

# @app.route("/order/delete_item", methods=["POST"])
# def delete_item():
#     return redirect("http://localhost:5001/order/delete_item")


# @app.route("/order/get_item", methods=["GET"])
# def order_get_item():
#     return redirect("http://localhost:5001/order/get_item")


# @app.route("/transaction/get_item", methods=["GET"])
# def transaction_get_item():
#     return redirect("http://localhost:5002/transaction/get_item")


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_1"
    app.run(debug=True)
