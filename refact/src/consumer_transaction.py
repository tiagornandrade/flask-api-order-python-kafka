import json
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from database.dbConnect import connectionRead, connectionWrite


connection_read = connectionRead()
connection_write = connectionWrite()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_transaction = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


class Transaction:
    def consumerTransactionCreated():
        while True:
            for message in consumer_transaction:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode("utf-8"))
                print(consumed_message)

                with connection_read:
                    data = consumed_message
                    id = data["id"]
                    transaction_id = str(uuid4())
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]

                    with connection_read.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO public.transaction VALUES (%s,%s) RETURNING transaction_id;",
                            (
                                transaction_id,
                                Json(
                                    {
                                        "id": id,
                                        "name": name,
                                        "description": description,
                                        "price": price,
                                    }
                                ),
                            ),
                        )

                with connection_write:
                    data = consumed_message
                    id = data["id"]
                    transaction_id = str(uuid4())
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]

                    with connection_write.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO public.transaction VALUES (%s,%s) RETURNING transaction_id;",
                            (
                                transaction_id,
                                Json(
                                    {
                                        "id": id,
                                        "name": name,
                                        "description": description,
                                        "price": price,
                                    }
                                ),
                            ),
                        )



if __name__ == "__main__":
    Transaction.consumerTransactionCreated()