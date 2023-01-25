import json
from kafka import KafkaProducer, KafkaConsumer

KAFKA_TOPIC = "order_details"

producer = KafkaProducer(retries=5, bootstrap_servers="localhost:9092")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    group_id="consumer-1",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)


def producerApi(content):
    future = producer.send(KAFKA_TOPIC, json.dumps(content).encode("utf-8"))
    producer.flush()
    future.get(timeout=60)
    return future
