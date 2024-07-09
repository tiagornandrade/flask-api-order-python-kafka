import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, JSON, String, DateTime

Base = declarative_base()


class PublicTransaction(Base):
    __tablename__ = "transactions"
    __table_args__ = {'schema': 'public'}
    transaction_id = Column(String, primary_key=True)
    transaction = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class RawTransaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'raw'}
    processed_at = Column(DateTime, primary_key=True)
    message_key = Column(String)
    message_value = Column(String, primary_key=True)
    payload = Column(JSON)