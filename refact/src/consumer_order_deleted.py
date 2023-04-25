import json
import datetime
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from database.dbConnect import connectionRead, connectionWrite


connection_read = connectionRead()
connection_write = connectionWrite()

ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


class Order:
    def consumerOrderDeleted():
        while True:
            for message in consumer_order_deleted:
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
                    created_at = None
                    updated_at = None
                    deleted_at = datetime.datetime.now()

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, created_at, updated_at, deleted_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, created_at, updated_at, deleted_at),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    created_at = None
                    updated_at = None
                    deleted_at = datetime.datetime.now()

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, name, description, price, created_at, updated_at, deleted_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, name, description, price, created_at, updated_at, deleted_at),
                        )
     

if __name__ == "__main__":
    Order.consumerOrderDeleted()