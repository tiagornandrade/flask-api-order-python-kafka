import json
from uuid import uuid4
from envyaml import EnvYAML
from database.dbConnect import connectionTransaction
from psycopg2.extras import Json

from kafka import KafkaConsumer
from kafka import KafkaProducer


env = EnvYAML("../../env.yaml")
connection = connectionTransaction()

bootstrap_servers = env["BOOTSTRAP_SERVER"]
ORDER_KAFKA_TOPIC = "order_details"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"

consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
producer_order = KafkaProducer(bootstrap_servers=bootstrap_servers)


def consumerTransactionApi():
    while True:
        for message in consumer:
            print("Gonna start listening..")
            print("Ongoing transaction..")
            consumed_message = json.loads(message.value.decode())
            print(consumed_message)
            with connection:
                data = consumed_message
                id = data["id"]
                transaction_id = str(uuid4())
                name = data["name"]
                description = data["description"]
                price = data["price"]

                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO public.transaction_created VALUES (%s,%s) RETURNING transaction_id;""",
                        (
                            transaction_id,
                            Json(
                                {
                                    "id": id,
                                    "name": name,
                                    "description": description,
                                    "price": price,
                                }
                            ),
                        ),
                    )
