import json
import datetime
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from database.dbConnect import connectionRead, connectionWrite


connection_read = connectionRead()
connection_write = connectionWrite()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


class Order:
    def consumerOrderCreated():
        while True:
            for message in consumer_order_created:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode("utf-8"))
                print(consumed_message)

                with connection_read:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    created_at = datetime.datetime.now()
                    updated_at = None
                    is_deleted = False

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, created_at, updated_at, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, created_at, updated_at, is_deleted),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    created_at = datetime.datetime.now()
                    updated_at = None
                    is_deleted = False

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, created_at, updated_at, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, created_at, updated_at, is_deleted),
                        )



if __name__ == "__main__":
    Order.consumerOrderCreated()