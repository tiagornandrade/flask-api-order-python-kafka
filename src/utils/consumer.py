import json
import datetime
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from dbConnect import connectionRead, connectionWrite


connection_read = connectionRead()
connection_write = connectionWrite()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"

bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_updated = KafkaConsumer(ORDER_UPDATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


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
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )

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
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )

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
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )

                with connection_write:
                    data = consumed_message
                    user_id = data["user_id"]
                    event_key = data["event_key"]
                    product_name = data["product_name"]
                    description = data["description"]
                    price = data["price"]
                    event_timestamp = datetime.datetime.now()
                    operation = data["operation"]

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                            (user_id, event_key, product_name, description, price, event_timestamp, operation),
                        )
