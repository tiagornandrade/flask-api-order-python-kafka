import json
import datetime
from kafka import KafkaConsumer
from dbConnect import connection_read, connection_write


ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(
    ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)
consumer_order_deleted = KafkaConsumer(
    ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)
consumer_order_updated = KafkaConsumer(
    ORDER_UPDATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)

connection_read = connection_read()
connection_write = connection_write()


class Order:
    @staticmethod
    def consume_messages(consumer):
        for message in consumer:
            print("Gonna start listening..")
            print("Ongoing transaction..")
            consumed_message = json.loads(message.value.decode("utf-8"))
            print(consumed_message)

            data = consumed_message
            user_id = data["user_id"]
            event_key = data["event_key"]
            product_name = data["product_name"]
            description = data["description"]
            price = data["price"]
            event_timestamp = datetime.datetime.now()
            operation = data["operation"]

            with connection_read, connection_read.cursor() as read_cursor:
                read_cursor.execute(
                    """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                    (
                        user_id,
                        event_key,
                        product_name,
                        description,
                        price,
                        event_timestamp,
                        operation,
                    ),
                )

            with connection_write, connection_write.cursor() as write_cursor:
                write_cursor.execute(
                    """INSERT INTO public.order (user_id, event_key, product_name, description, price, event_timestamp, operation) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;""",
                    (
                        user_id,
                        event_key,
                        product_name,
                        description,
                        price,
                        event_timestamp,
                        operation,
                    ),
                )

    @staticmethod
    def consumer_order_created():
        Order.consume_messages(consumer_order_created)

    @staticmethod
    def consumer_order_deleted():
        Order.consume_messages(consumer_order_deleted)

    @staticmethod
    def consumer_order_updated():
        Order.consume_messages(consumer_order_updated)
