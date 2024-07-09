from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Sequence

Base = declarative_base()


class PublicOrder(Base):
    __tablename__ = "orders"
    __table_args__ = {'schema': 'public'}
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    order_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    event_key = Column(String)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float)
    event_timestamp = Column(DateTime)
    operation = Column(String)


class RawOrder(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'raw'}
    processed_at = Column(DateTime, primary_key=True)
    message_key = Column(String)
    message_value = Column(String, primary_key=True)
    payload = Column(JSON)
