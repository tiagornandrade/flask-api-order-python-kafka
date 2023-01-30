import json
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
    future = producer.send(KAFKA_TOPIC, json.dumps(content).encode("utf-8"))
    producer.flush()
    future.get(timeout=60)
    return future
