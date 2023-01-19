from flask import Flask
from routes.item_route import item_route


app = Flask(__name__)
app.register_blueprint(item_route)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5001)
    app.run()
    app.secret_key = "app3"