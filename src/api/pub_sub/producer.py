import json
from uuid import uuid4
from envyaml import EnvYAML
from kafka import KafkaProducer
from dataclasses import dataclass

env = EnvYAML("../../env.yaml")
ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = env["BOOTSTRAP_SERVER"]

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)


@dataclass
class MessageCreated:
    id: str
    name: str
    description: str
    price: float


@dataclass
class MessageDeleted:
    id: str
    id_created: str
    name: str
    description: str
    price: float


def producerCreated(content):
    data = content
    msg_created = MessageCreated(
        str(uuid4()), data["name"], data["description"], data["price"]
    )
    message = {
        "id": msg_created.id,
        "name": msg_created.name,
        "description": msg_created.description,
        "price": msg_created.price,
    }
    future = producer_order.send(
        ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    producer_order.flush()
    future.get(timeout=60)
    return future


def producerDeleted(content):
    data = content
    msg_deleted = MessageDeleted(
        str(uuid4()), data["id"], data["name"], data["description"], data["price"]
    )
    message = {
        "id": msg_deleted.id,
        "id_created": msg_deleted.id_created,
        "name": msg_deleted.name,
        "description": msg_deleted.description,
        "price": msg_deleted.price,
        "is_deleted": True,
    }
    future = producer_order.send(
        ORDER_DELETED_KAFKA_TOPIC, json.dumps(message).encode("utf-8")
    )
    producer_order.flush()
    future.get(timeout=60)
    return future
