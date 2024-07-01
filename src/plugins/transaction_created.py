import os
import json
from uuid import uuid4
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from dotenv import load_dotenv

load_dotenv()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
ORDER_DELETED_KAFKA_TOPIC = "order_deleted"
ORDER_CONFIRMED_KAFKA_TOPIC = "order_confirmed"
bootstrap_servers = "localhost:9092"

consumer_order_created = KafkaConsumer(
    ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)
consumer_order_deleted = KafkaConsumer(
    ORDER_DELETED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)
consumer_transaction = KafkaConsumer(
    ORDER_CREATED_KAFKA_TOPIC, bootstrap_servers=bootstrap_servers
)

ENGINE = os.environ.get("ENGINE_DATABASE_URL")

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)

class Transaction:
    @staticmethod
    def consumerTransactionCreated():
        session = Session()
        while True:
            for message in consumer_transaction:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode("utf-8"))
                print(consumed_message)

                data = consumed_message
                id = data["id"]
                transaction_id = str(uuid4())
                name = data["name"]
                description = data["description"]
                price = data["price"]

                transaction_data = {
                    "transaction_id": transaction_id,
                    "data": json.dumps({
                        "id": id,
                        "name": name,
                        "description": description,
                        "price": price
                    })
                }

                try:
                    session.execute(
                        text("""INSERT INTO public.transaction (transaction_id, data) 
                                VALUES (:transaction_id, :data) 
                                RETURNING transaction_id;"""),
                        transaction_data
                    )
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"Error inserting transaction: {e}")
                finally:
                    session.close()

if __name__ == "__main__":
    Transaction.consumerTransactionCreated()
