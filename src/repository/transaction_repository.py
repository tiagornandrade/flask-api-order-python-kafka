import os
from sqlalchemy import create_engine
from src.entity.transaction_entity import Transaction
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

ENGINE = os.environ.get("ENGINE1_DATABASE_URL")

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class TransactionRepository:
    def __init__(self):
        self.session = Session()

    def get_all_transactions(self):
        transactions = self.session.query(Transaction).all()
        result = []
        for transaction in transactions:
            transaction_data = {
                'transaction_id': transaction.transaction_id,
                'transaction': transaction.transaction
            }
            result.append(transaction_data)
        return result
