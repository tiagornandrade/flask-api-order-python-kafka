import json
from uuid import uuid4
from kafka import KafkaProducer
from dataclasses import dataclass


ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

producer_order = KafkaProducer(
    retries=5,
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


@dataclass
class Message:
    user_id: str
    event_key: str
    product_name: str
    description: str
    price: float
    operation: str


def produce_message(message_type, data):
    msg = Message(
        str(uuid4()),
        str(uuid4()),
        data["name"],
        data["description"],
        data["price"],
        message_type,
    )

    topic = {
        "created": ORDER_CREATED_KAFKA_TOPIC,
        "updated": ORDER_UPDATED_KAFKA_TOPIC,
        "deleted": ORDER_DELETED_KAFKA_TOPIC,
    }.get(message_type)

    future = producer_order.send(topic, msg.__dict__)
    producer_order.flush()
    future.get(timeout=60)
    return future
