import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, JSON, String


ENGINE = os.environ.get("ENGINE")

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id = Column(String, primary_key=True)
    transaction = Column(JSON)



def transactionGetItem():
    engine = create_engine(ENGINE)
    Session = sessionmaker(bind=engine)
    session = Session()

    transactions = session.query(Transaction).all()

    result = []
    for transaction in transactions:
        transaction_data = {
            'transaction_id': transaction.transaction_id,
            'transaction': transaction.transaction
        }
        result.append(transaction_data)

    return result