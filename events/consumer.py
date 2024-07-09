import os
import json
from uuid import uuid4
from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.entities.order_entity import RawOrder
from src.entities.transaction_entity import PublicTransaction, RawTransaction

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
        
        while True:
            for message in consumer:
                session = Session()
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

                transaction_data = PublicTransaction(
                    transaction_id=transaction_id,
                    transaction={
                        "id": id,
                        "name": name,
                        "description": description,
                        "price": price
                    }
                )

                try:
                    session.add(transaction_data)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"Error inserting transaction: {e}")

                raw_transaction_data = RawTransaction(
                    processed_at=datetime.now(),
                    message_key="uuid",
                    message_value=str(uuid4()),
                    payload={
                        "transaction_id": transaction_id,
                        "transaction": {
                            "id": id,
                            "name": name,
                            "description": description,
                            "price": price
                        }
                    }
                )

                try:
                    session.add(raw_transaction_data)
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(f"Error inserting raw transaction: {e}")

                raw_order_data = RawOrder(
                    processed_at=datetime.now(),
                    message_key="uuid",
                    message_value=str(uuid4()),
                    payload={
                        "id": id,
                        "name": name,
                        "description": description,
                        "price": price
                    }
                )

                try:
                    session.add(raw_order_data)
                    session.commit()
                    print("Transaction committed.")
                except Exception as e:
                    session.rollback()
                    print(f"Error inserting raw order: {e}")    
                finally:
                    session.close()
