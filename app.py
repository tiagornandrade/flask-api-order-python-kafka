import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from uuid import uuid4
from flask import Flask, request, jsonify
import requests
import json

load_dotenv()

app = Flask(__name__)

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)

CREATE_ROOMS_TABLE = ("CREATE TABLE IF NOT EXISTS items_by_id (id SERIAL PRIMARY KEY, name TEXT, description TEXT, price FLOAT);")
INSERT_ROOM_RETURN_ID = "INSERT INTO items_by_id (id, name, description, price) VALUES (%s,%s,%s,%s) RETURNING id;"
GET_ID = ("""SELECT * FROM items_by_id;""")

@app.route("/", methods=["GET","POST"])
def create_event():
    data        = request.get_json()
    id          = str(uuid4())
    name        = data["name"]
    description = data["description"]
    price       = data["price"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (id,name,description,price))
            id = cursor.fetchone()[0]
    return {"id": id, "name": f"{name} created."}, 201

@app.route("/get_itens", methods=["GET"])
def open_event():
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(GET_ID)
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
    app.secret_key = "app"
    app.run(debug=True)