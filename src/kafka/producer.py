import json
from urllib.request import urlopen

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "order_details"

producer = KafkaProducer(retries=5, bootstrap_servers="localhost:9092")

url = "http://localhost:5000/test"
response = urlopen(url)
data = json.loads(response.read())

while True:
    print("sending message...")
    future = producer.send(ORDER_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))
    producer.flush()
    future.get(timeout=60)
    print("message sent successfully...")
