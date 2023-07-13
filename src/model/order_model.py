from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime



Base = declarative_base()

class Order(Base):
    __tablename__ = 'order'
    user_id = Column(String, primary_key=True)
    event_key = Column(String)
    product_name = Column(String)
    description = Column(String)
    price = Column(Float)
    event_timestamp = Column(DateTime)
    operation = Column(String)



def orderGetItem():
    engine = create_engine('postgresql://postgres:postgres@localhost:54322/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()

    orders = session.query(Order).all()

    result = []
    for order in orders:
        order_data = {
            'user_id': order.user_id,
            'event_key': order.event_key,
            'product_name': order.product_name,
            'description': order.description,
            'price': order.price,
            'event_timestamp': order.event_timestamp.isoformat(),
            'operation': order.operation
        }
        result.append(order_data)

    return result