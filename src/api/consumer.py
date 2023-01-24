import os
import json
import psycopg2
from uuid import uuid4
from psycopg2.extras import Json

from kafka import KafkaConsumer
from kafka import KafkaProducer

# url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect('postgresql://localhost/market_db')

ORDER_KAFKA_TOPIC = "order_details"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"

consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers="localhost:9092")
producer_order = KafkaProducer(bootstrap_servers="localhost:9092")

while True:
    for message in consumer:
        print("Gonna start listening..")
        print("Ongoing transaction..")
        consumed_message = json.loads(message.value.decode())
        print(consumed_message)
        with connection:
            data        = consumed_message
            id          = str(uuid4())
            transaction_id = str(uuid4())
            name        = data["name"]
            description = data["description"]
            price       = data["price"]

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO market_db.public.order (id, name, description, price) VALUES (%s,%s,%s,%s) RETURNING id;""", (id,name,description,price))
                cursor.execute("""INSERT INTO market_db.public.transaction VALUES (%s,%s) RETURNING trsansaction_id;""", (transaction_id, Json({'id':id,'name':name,'description':description,'price':price})))