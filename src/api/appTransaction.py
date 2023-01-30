from flask import Flask
from routes.transaction import transactionGetItem


app = Flask(__name__)


@app.route("/transaction/get_item", methods=["GET"])
def transaction_get_item():
    return transactionGetItem()


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_transaction"
    app.run(debug=True, port=5001)
