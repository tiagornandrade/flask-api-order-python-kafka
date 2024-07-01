import secrets
from flask import Flask

from src.controller import routes

app = Flask(__name__)
routes.init_app(app)

app.secret_key = secrets.token_hex(16)


if __name__ == "__main__":
    app.run(debug=True)
