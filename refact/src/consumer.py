import json
from kafka import KafkaConsumer


ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


def consumerOrder():
    while True:
        for message in consumer_order_created:
            print("Gonna start listening..")
            print("Ongoing transaction..")
            consumed_message = json.loads(message.value.decode())
            print(consumed_message)


if __name__ == "__main__":
    consumerOrder()