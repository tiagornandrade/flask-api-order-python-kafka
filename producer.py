import json
import time
import requests

from kafka import KafkaProducer

response = requests.get('http://localhost:5000/test').text


ORDER_KAFKA_TOPIC = "order_details"
ORDER_LIMIT = 15

producer = KafkaProducer(retries=5, bootstrap_servers='localhost:9092')

data = json.loads(response)

producer.send(
    ORDER_KAFKA_TOPIC,
    json.dumps(data).encode("utf-8")
)
producer.flush()