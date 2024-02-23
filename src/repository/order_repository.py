import os
from sqlalchemy import create_engine
from src.entity.order_entity import Order
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

ENGINE = os.environ.get("ENGINE1_DATABASE_URL")

engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


class OrderRepository:
    def __init__(self):
        self.session = Session()

    def create_order(self, order_data):
        order = Order(**order_data)
        self.session.add(order)
        self.session.commit()
        return order.user_id

    def get_all_orders(self):
        orders = self.session.query(Order).all()
        result = []
        for order in orders:
            order_data = {
                "order_id": order.order_id,
                "event_key": order.event_key,
                "product_name": order.product_name,
                "description": order.description,
                "price": order.price,
                "event_timestamp": order.event_timestamp.isoformat(),
                "operation": order.operation,
            }
            result.append(order_data)
        return result

    def get_order_by_id(self, id):
        try:
            order = self.session.query(Order).filter_by(order_id=id).first()
            if order:
                return {
                    "order_id": order.order_id,
                    "event_key": order.event_key,
                    "product_name": order.product_name,
                    "description": order.description,
                    "price": order.price,
                    "event_timestamp": order.event_timestamp,
                    "operation": order.operation,
                }
        except Exception as e:
            self.session.rollback()
            print(f"Error fetching order by id: {e}")
        return None

    def update_order(self, user_id, updated_data):
        order = self.session.query(Order).filter_by(user_id=user_id).first()
        if order:
            for key, value in updated_data.items():
                setattr(order, key, value)
            self.session.commit()
            return True
        return False

    def delete_order(self, user_id):
        order = self.session.query(Order).filter_by(user_id=user_id).first()
        if order:
            self.session.delete(order)
            self.session.commit()
            return True
        return False
