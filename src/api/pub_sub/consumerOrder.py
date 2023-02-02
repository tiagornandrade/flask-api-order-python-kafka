import json
from uuid import uuid4
from envyaml import EnvYAML
from database.dbConnect import connectionOrder
from psycopg2.extras import Json

from kafka import KafkaConsumer
from kafka import KafkaProducer


env = EnvYAML("../../env.yaml")
connection = connectionOrder()

bootstrap_servers = env["BOOTSTRAP_SERVER"]
ORDER_KAFKA_TOPIC = "order_details"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"

consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
producer_order = KafkaProducer(bootstrap_servers=bootstrap_servers)


def consumerOrderApi():
    while True:
        for message in consumer:
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
                        """INSERT INTO public.order_created (id, name, description, price) VALUES (%s,%s,%s,%s) RETURNING id;""",
                        (id, name, description, price),
                    )
