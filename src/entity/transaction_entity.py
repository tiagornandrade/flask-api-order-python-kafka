from sqlalchemy import create_engine, Column, JSON, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(String, primary_key=True)
    transaction = Column(JSON)