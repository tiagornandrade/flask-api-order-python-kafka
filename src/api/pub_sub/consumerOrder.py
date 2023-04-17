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
                    is_created = True
                    is_updated = False
                    is_deleted = False

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (id, name, description, price, is_created, is_updated, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price, is_created, is_updated, is_deleted),
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
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    is_created = False
                    is_updated = False
                    is_deleted = True

                    with connection.cursor() as cursor:
                        cursor.execute(
                             """INSERT INTO public.order (id, name, description, price, is_created, is_updated, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price, is_created, is_updated, is_deleted),
                        )
