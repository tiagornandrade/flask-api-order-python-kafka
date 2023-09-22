from flask import Flask, request, jsonify
from src.model.order_model import orderGetItem
from src.model.transaction_model import transactionGetItem
from confluent_kafka import Producer
from datetime import datetime

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)


def init_app(app: Flask):
    @app.route('/create', methods=['POST'])
    def create():
        data = request.json
        producer.produce('my_topic', key='create', value=str({'payload': [data], 'is_deleted': False, 'created_at': datetime.now()}))
        producer.flush()
        return jsonify({'message': 'Created successfully'}), 201


    @app.route('/update/<int:id>', methods=['PUT'])
    def update(id):
        data = request.json
        producer.produce('my_topic', key='update', value=str({'id': id, 'data': data, 'is_deleted': False}))
        producer.flush()
        return jsonify({'message': f'Updated {id} successfully'}), 200


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
