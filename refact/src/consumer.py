import json
import datetime
from uuid import uuid4
from kafka import KafkaConsumer
from psycopg2.extras import Json
from database.dbConnect import connectionRead


connection = connectionRead()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_order_deleted = KafkaConsumer(ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)
consumer_transaction = KafkaConsumer(ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers)


class Order:
    def consumerOrder():
        while True:
            for message in consumer_order_created:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)

                with connection:
                    data = consumed_message
                    id = data["id"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    created_at = datetime.datetime.now()
                    updated_at = None
                    is_deleted = False

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.order (id, name, description, price, created_at, updated_at, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price, created_at, updated_at, is_deleted),
                        )

    def consumerOrderUpdated():
        while True:
            for message in consumer_order_deleted:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)
                with connection:
                    data = consumed_message
                    id = data["id"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    is_created = False
                    is_updated = False
                    is_deleted = True

                    with connection.cursor() as cursor:
                        cursor.execute(
                             """INSERT INTO public.order (id, name, description, price, is_created, is_updated, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price, is_created, is_updated, is_deleted),
                        )
    
    def consumerOrderDeleted():
        while True:
            for message in consumer_order_deleted:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)
                with connection:
                    data = consumed_message
                    id = data["id"]
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]
                    is_created = False
                    is_updated = False
                    is_deleted = True

                    with connection.cursor() as cursor:
                        cursor.execute(
                             """INSERT INTO public.order (id, name, description, price, is_created, is_updated, is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id;""",
                            (id, name, description, price, is_created, is_updated, is_deleted),
                        )

class Transaction:
    def consumerTransactionCreated():
        while True:
            for message in consumer_transaction:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode())
                print(consumed_message)
                with connection:
                    data = consumed_message
                    id = data["id"]
                    transaction_id = str(uuid4())
                    name = data["name"]
                    description = data["description"]
                    price = data["price"]

                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO public.transaction_created VALUES (%s,%s) RETURNING transaction_id;""",
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
    Order.consumerOrder()
    Transaction.consumerTransactionCreated()