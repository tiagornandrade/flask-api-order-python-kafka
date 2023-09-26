import os
from sqlalchemy import create_engine, Column, JSON, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

ENGINE = os.environ.get("ENGINE1_DATABASE_URL")

Base = declarative_base()
engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(String, primary_key=True)
    transaction = Column(JSON)


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
