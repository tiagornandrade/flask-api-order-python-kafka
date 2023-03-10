import json
from uuid import uuid4
from envyaml import EnvYAML
from database.dbConnect import connectionRead
from psycopg2.extras import Json

from kafka import KafkaConsumer


env = EnvYAML("../../env.yaml")
connection = connectionRead()

bootstrap_servers = env["BOOTSTRAP_SERVER"]
ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)

class Order:
    def consumerOrderCreated():
        while True:
            for message in consumer_order_created:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)
                with connection:
                    data = consumed_message
                    id = data["id"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (id, name, description, price) VALUES (%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price),
                        )
    
    def consumerOrderDeleted():
        while True:
            for message in consumer_order_deleted:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)
                with connection:
                    data = consumed_message
                    id = data["id"]
                    id_created = data["id_created"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    is_deleted = True

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order_deleted (id, id_created, name, description, price, is_deleted) VALUES (%s,%s,%s,%s,%s, %s) RETURNING id;""",
                            (id, id_created, name, description, price, is_deleted),
                        )
