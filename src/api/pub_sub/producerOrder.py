import json
from uuid import uuid4
from envyaml import EnvYAML
from kafka import KafkaProducer, KafkaConsumer

env = EnvYAML("../../env.yaml")
KAFKA_TOPIC = "order_details"
bootstrap_servers = env["BOOTSTRAP_SERVER"]

producer = KafkaProducer(retries=5, bootstrap_servers=bootstrap_servers)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    group_id="consumer-1",
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)


def producerApi(content):
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
    future = producer.send(KAFKA_TOPIC, json.dumps(message).encode("utf-8"))
    producer.flush()
    future.get(timeout=60)
    return future
