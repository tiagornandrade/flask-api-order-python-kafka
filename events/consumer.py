import os
import json
from uuid import uuid4
from dotenv import load_dotenv
from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text

load_dotenv()

ORDER_CREATED_KAFKA_TOPIC = "order_created"
bootstrap_servers = "localhost:9092"

engine = create_engine(os.environ.get("ENGINE_DATABASE_URL"))
Session = sessionmaker(bind=engine)


class Transaction:
    @staticmethod
    def consumer_transaction_created(only_create=False):
        consumer = KafkaConsumer(
            ORDER_CREATED_KAFKA_TOPIC, 
            bootstrap_servers=bootstrap_servers,
            group_id='my-group-id'
        )
        session = Session()
        
        while True:
            for message in consumer:
                print("Gonna start listening..")
                print("Ongoing transaction..")
                consumed_message = json.loads(message.value.decode("utf-8"))
                print(consumed_message)

                if only_create and message.key != b"create":
                    continue

                data = consumed_message["payload"]
                id = data["order_id"]
                transaction_id = str(uuid4())
                name = data["product_name"]
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
                        text("""INSERT INTO public.transactions (transaction_id, transaction) 
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