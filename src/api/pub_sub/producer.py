import json
from uuid import uuid4
from envyaml import EnvYAML
from kafka import KafkaProducer

env = EnvYAML("../../env.yaml")
ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = env["BOOTSTRAP_SERVER"]

producer_order = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)


def producerCreated(content):
    data = content
    id = str(uuid4())
    name = data["name"]
    description = data["description"]
    price = data["price"]
    message = {
            "id": id,
            "name": name,
            "description": description,
            "price": price
    }
    future = producer_order.send(ORDER_CREATED_KAFKA_TOPIC, json.dumps(message).encode("utf-8"))
    producer_order.flush()
    future.get(timeout=60)
    return future

def producerDeleted(content):
    data = content
    id = str(uuid4())
    id_created = data["id"]
    name = data["name"]
    description = data["description"]
    price = data["price"]
    message = {
            "id": id,
            "id_created": id_created,
            "name": name,
            "description": description,
            "price": price,
            "is_deleted": True
    }
    future = producer_order.send(ORDER_DELETED_KAFKA_TOPIC, json.dumps(message).encode("utf-8"))
    producer_order.flush()
    future.get(timeout=60)
    return future
