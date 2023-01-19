import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "order_details"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"

consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers="localhost:9092")
producer = KafkaProducer(bootstrap_servers="localhost:9092")

print("Gonna start listening..")
while True:
    for message in consumer:
        print("Ongoing transaction..")
        consumed_message = json.loads(message.value.decode())
        print(consumed_message)