from flask import Flask, request, jsonify
from src.model.order_model import orderGetItem
from src.model.transaction_model import transactionGetItem
from confluent_kafka import Producer
from datetime import datetime
import redis
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


def init_app(app: Flask):
    @app.route('/create', methods=['POST'])
    def create():
        data = request.json

        redis_key = f"item_{data['id']}"
        redis_client.set(redis_key, json.dumps(data))

        kafka_payload = {
            'payload': data,
            'is_deleted': False,
            'created_at': datetime.now().isoformat()
        }
        producer.produce('my_topic', key='create', value=json.dumps(kafka_payload))
        producer.flush()

        return jsonify({'message': 'Created successfully'}), 201

    @app.route('/update/<int:id>', methods=['PUT'])
    def update(id):
        data = request.json

        redis_key = f"item_{id}"

        if redis_client.exists(redis_key):
            updated_data = {"id": id, **data}
            redis_client.set(redis_key, json.dumps(updated_data))
            redis_value = redis_client.get(redis_key)

            kafka_payload = {
                'payload': json.loads(redis_value),
                'is_deleted': False,
                'updated_at': datetime.now().isoformat()
            }
            producer.produce('my_topic', key='update', value=json.dumps(kafka_payload))
            producer.flush()

            return jsonify({'message': f'Updated {id} successfully'}), 200
        else:
            return jsonify({'error': 'Item not found in Redis'}), 404

    @app.route('/delete/<int:id>', methods=['DELETE'])
    def delete(id):
        producer.produce('my_topic', key='delete', value=str({'id': id, 'is_deleted': True}))
        producer.flush()
        return jsonify({'message': f'Deleted {id} successfully'}), 200

    @app.route('/list', methods=['GET'])
    def list_items():
        items = [{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}]
        producer.produce('my_topic', key='list', value=str(items))
        producer.flush()
        return jsonify(items), 200


if __name__ == '__main__':
    app.run(debug=True)
