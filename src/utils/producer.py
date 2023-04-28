import json
from uuid import uuid4
from kafka import KafkaProducer
from dataclasses import dataclass


ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_UPDATED_KAFKA_TOPIC = "order_updated"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)

@dataclass
class MessageCreated:
    user_id: str
    event_key: str
    product_name: str
    description: str
    price: float
    operation: str

@dataclass
class MessageDeleted:
    user_id: str
    event_key: str
    product_name: str
    description: str
    price: float
    operation: str

@dataclass
class MessageUpdated:
    user_id: str
    event_key: str
    product_name: str
    description: str
    price: float
    operation: str


def producerCreated(message):
    data = message
    msg_created = MessageCreated(
        str(uuid4()), str(uuid4()), data["product_name"], data["description"], data["price"], str("POST")
    )
    message = {
        "user_id": msg_created.user_id,
        "event_key": msg_created.event_key,
        "product_name": msg_created.product_name,
        "description": msg_created.description,
        "price": msg_created.price,
        "operation": msg_created.price,
    }

    future = producer_order.send(
        ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    producer_order.flush()
    future.get(timeout=60)
    return future


def producerDeleted(message):
    data = message
    msg_created = MessageCreated(
        str(uuid4()), str(uuid4()), data["product_name"], data["description"], data["price"], str("DELETE")
    )
    message = {
        "user_id": msg_created.user_id,
        "event_key": msg_created.event_key,
        "product_name": msg_created.product_name,
        "description": msg_created.description,
        "price": msg_created.price,
        "operation": msg_created.price,
    }

    future = producer_order.send(
        ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    producer_order.flush()
    future.get(timeout=60)
    return future


def producerUpdated(message):
    data = message
    msg_created = MessageCreated(
        str(uuid4()), str(uuid4()), data["product_name"], data["description"], data["price"], str("PUT")
    )
    message = {
        "user_id": msg_created.user_id,
        "event_key": msg_created.event_key,
        "product_name": msg_created.product_name,
        "description": msg_created.description,
        "price": msg_created.price,
        "operation": msg_created.price,
    }

    future = producer_order.send(
        ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    producer_order.flush()
    future.get(timeout=60)
    return future
