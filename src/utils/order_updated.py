import json
import datetime
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from dbConnect import connectionRead, connectionWrite


connection_read = connectionRead()
connection_write = connectionWrite()

ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
bootstrap_servers = "localhost:9092"

consumer_order_updated = KafkaConsumer(ORDER_UPDATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


class Order:
    def consumerOrderUpdated():
        while True:
            for message in consumer_order_updated:
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
                    event_timestamp = datetime.datetime.now()
                    method = data["method"]

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, event_timestamp, method) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, event_timestamp, method),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    method = data["method"]

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, event_timestamp, method) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, event_timestamp, method),
                        )
     

if __name__ == "__main__":
    Order.consumerOrderUpdated()