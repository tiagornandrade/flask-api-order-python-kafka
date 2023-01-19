import json
from flask import Flask


app = Flask(__name__)


from kafka import KafkaProducer, KafkaConsumer

ORDER_KAFKA_TOPIC = "order_details"

producer = KafkaProducer(retries=5, bootstrap_servers='localhost:9092')
consumer = KafkaConsumer(ORDER_KAFKA_TOPIC, bootstrap_servers='localhost:9092')

@app.route("/get_item", methods=["GET"])
def get_item():
    for message in consumer:
        print("Ongoing transaction..")
        consumed_message = json.loads(message.value.decode())
        print(consumed_message)

if __name__ == "__main__":
    app.secret_key = "app2_1"
    app.run(debug=True, host='0.0.0.0', port=5001)