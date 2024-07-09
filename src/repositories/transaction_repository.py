import os
from sqlalchemy import create_engine
from src.entities.transaction_entity import PublicTransaction
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json

load_dotenv()

ENGINE = os.environ.get("ENGINE_DATABASE_URL")

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class TransactionRepository:
    def __init__(self):
        self.session = Session()

    def get_all_transactions(self):
        transactions = self.session.query(PublicTransaction).all()
        result = []
        for transaction in transactions:
            transaction_data = {
                "transaction_id": transaction.transaction_id,
                "transaction": transaction.transaction,
            }
            result.append(transaction_data)
        return result
    