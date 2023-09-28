from flask import Flask

from src.controller import routes

app = Flask(__name__)
routes.init_app(app)


if __name__ == "__main__":
    app.secret_key = "app_flask_kafka_1"
    app.run(debug=True)
