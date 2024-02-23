from pub_sub.producer import producerCreated, producerDeleted
from stream.dbConnect import connectionWrite
from psycopg2.extras import DictCursor
import datetime
from flask import Flask, request, jsonify, redirect
from routes.order import orderGetItem, orderGetItemById
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
        created_at = datetime.datetime.now()

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO public.order (id, name, description, price, created_at) VALUES (%s,%s,%s,%s,%s) RETURNING id;""",
                (id, name, description, price, created_at),
            )
            connection.commit()

        producerCreated(content)
    return jsonify(content)


@app.route("/order/delete_item/<id>", methods=["DELETE"])
def delete_item(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM public.order WHERE id =%s;", (id,))
        connection.commit()

    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM public.order WHERE id=%s;", (id,))
            get_itens = cursor.fetchall()
            cursor.close()
            response_itens = [row_to_dict_order(x) for x in get_itens]
    producerDeleted(response_itens)
    return jsonify({"registry": "deleted"})


@app.route("/order/get_item", methods=["GET"])
def order_get_item():
    return orderGetItem()


@app.route("/order/get_item/<id>", methods=["GET"])
def order_get_item_by_id(id):
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM public.order WHERE id=%s;", (id,))
            get_itens = cursor.fetchall()
            cursor.close()
            response_itens = [row_to_dict_order(x) for x in get_itens]
    return response_itens


def row_to_dict_order(row):
    return dict(
        {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"],
            "price": row["price"],
            "created_at": row["created_at"],
        }
    )


# @app.route("/order/update_item", methods=["PUT"])
# def order_update_item():
#     return orderUpdateItem()


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_write"
    app.run(debug=True, port=5001)
