import json
import time

from kafka import KafkaProducer

ORDER_KAFKA_TOPIC = "order_details"
ORDER_LIMIT = 15

producer = KafkaProducer(boostrap_servers="localhost:9092")

print("Going to be generating order after 10 seconds")
print("Will generate one unique order by 10 seconds")

for i in range(1, ORDER_LIMIT):
    data = {
        "order_id": i,
        "user_id": f"tom_{i}"
        "total_cost": i
    }