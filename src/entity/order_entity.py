from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Sequence

Base = declarative_base()


class Order(Base):
    __tablename__ = 'order'

    user_id = Column(Integer, primary_key=True)
    order_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    event_key = Column(String)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float)
    event_timestamp = Column(DateTime)
    operation = Column(String)
