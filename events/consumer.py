import os
import json
import datetime
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


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

ENGINE = os.environ.get("ENGINE_DATABASE_URL")

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class Order:
    @staticmethod
    def consume_messages(consumer):
        session = Session()
        for message in consumer:
            print("Gonna start listening..")
            print("Ongoing transaction..")
            consumed_message = json.loads(message.value.decode("utf-8"))
            print(consumed_message)

            data = consumed_message
            user_id = data.get("user_id")
            event_key = data.get("event_key")
            product_name = data.get("product_name")
            description = data.get("description")
            price = data.get("price")
            event_timestamp = datetime.datetime.now()
            operation = data.get("operation")

            order_data = {
                "user_id": user_id,
                "event_key": event_key,
                "product_name": product_name,
                "description": description,
                "price": price,
                "event_timestamp": event_timestamp,
                "operation": operation,
            }

            try:
                session.execute(
                    """INSERT INTO public.orders (user_id, event_key, product_name, description, price, event_timestamp, operation)
                       VALUES (:user_id, :event_key, :product_name, :description, :price, :event_timestamp, :operation)
                       RETURNING user_id;""",
                    order_data
                )
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error inserting order: {e}")
            finally:
                session.close()

    @staticmethod
    def consumer_order_created():
        Order.consume_messages(consumer_order_created)

    @staticmethod
    def consumer_order_deleted():
        Order.consume_messages(consumer_order_deleted)

    @staticmethod
    def consumer_order_updated():
        Order.consume_messages(consumer_order_updated)
