from flask import Flask, request, jsonify
from model.order_model import OrderRepository
from model.transaction_model import TransactionRepository
from confluent_kafka import Producer
from datetime import datetime
import redis
import uuid
import json

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'localhost:9092',
}
producer = Producer(conf)

redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

order_repo = OrderRepository()
transaction_repo = TransactionRepository()


def init_app(app: Flask):

    @app.route('/order', methods=['POST'])
    def create_order():
        data = request.json
        order_id = str(uuid.uuid4())
        redis_key = f"item_{order_id}"
        data['order_id'] = order_id
        redis_client.set(redis_key, json.dumps(data))

        kafka_payload = {
            'payload': data,
            'is_deleted': False,
            'created_at': datetime.now().isoformat()
        }
        producer.produce('my_topic', key='create', value=json.dumps(kafka_payload))
        producer.flush()

        order_repo.create_order(data)
        return jsonify({'id': order_id}), 201

    @app.route('/order/<string:id>', methods=['GET'])
    def get_order(id):
        order = order_repo.get_order_by_id(id)
        if order:
            return jsonify(order), 200
        return jsonify({'error': 'Order not found'}), 404

    @app.route('/order/<string:user_id>', methods=['PUT'])
    def update_order(user_id):
        data = request.json
        redis_key = f"item_{user_id}"
        redis_client.set(redis_key, json.dumps(data))

        kafka_payload = {
            'payload': data,
            'is_deleted': False,
            'updated_at': datetime.now().isoformat()
        }
        producer.produce('my_topic', key='update', value=json.dumps(kafka_payload))
        producer.flush()

        success = order_repo.update_order(user_id, data)
        if success:
            return jsonify({'message': 'Updated successfully'}), 200
        return jsonify({'error': 'Update failed'}), 400

    @app.route('/order/<string:order_id>', methods=['DELETE'])
    def delete_order(order_id):
        producer.produce('my_topic', key='delete', value=str({'id': order_id, 'is_deleted': True}))
        producer.flush()
        success = order_repo.delete_order(order_id)
        if success:
            return jsonify({'message': 'Deleted successfully'}), 200
        return jsonify({'error': 'Delete failed'}), 400

    @app.route('/orders', methods=['GET'])
    def get_all_orders():
        return jsonify(order_repo.get_all_orders()), 200

    @app.route('/transactions', methods=['GET'])
    def get_all_transactions():
        return jsonify(transaction_repo.get_all_transactions()), 200


if __name__ == '__main__':
    init_app(app)
    app.run(debug=True)
