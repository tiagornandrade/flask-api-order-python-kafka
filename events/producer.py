import json
from confluent_kafka import Producer
from datetime import datetime
import uuid


bootstrap_servers = "localhost:9092"
producer = Producer({"bootstrap.servers": bootstrap_servers})


def produce_message(topic, key, value):
    producer.produce(topic, key=key, value=value)
    producer.flush()


def produce_create_order_message(data):
    order_id = str(uuid.uuid4())
    data["order_id"] = order_id

    kafka_payload = {
        "payload": data,
        "is_deleted": False,
        "created_at": datetime.now().isoformat(),
    }

    produce_message("order_created", key="create", value=json.dumps(kafka_payload))
    return order_id


def produce_update_order_message(user_id, data):

    kafka_payload = {
        "payload": data,
        "is_deleted": False,
        "updated_at": datetime.now().isoformat(),
    }

    produce_message("order_updated", key="update", value=json.dumps(kafka_payload))
    return True


def produce_delete_order_message(order_id):
    produce_message("order_deleted", key="delete", value=str({"id": order_id, "is_deleted": True}))
    return True
