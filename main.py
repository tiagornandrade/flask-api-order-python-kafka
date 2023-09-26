from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configurações do banco de dados
DATABASE_URL = 'postgresql://postgres:postgres@localhost/postgres'

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))


class MyModel(Base):
    __tablename__ = 'my_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


Base.metadata.create_all(engine)


@app.route('/create', methods=['POST'])
def create():
    session = Session()
    data = request.json
    new_item = MyModel(name=data['name'])
    session.add(new_item)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({'message': 'Error creating the item'}), 400
    finally:
        session.close()
    return jsonify({'message': 'Created successfully', 'id': new_item.id}), 201


@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    session = Session()
    data = request.json
    item = session.query(MyModel).get(id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    item.name = data['name']
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({'message': 'Error updating the item'}), 400
    finally:
        session.close()
    return jsonify({'message': 'Updated successfully'}), 200


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    session = Session()
    item = session.query(MyModel).get(id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404
    session.delete(item)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({'message': 'Error deleting the item'}), 400
    finally:
        session.close()
    return jsonify({'message': 'Deleted successfully'}), 200


@app.route('/list', methods=['GET'])
def list_items():
    session = Session()
    items = session.query(MyModel).all()
    session.close()
    return jsonify([{'id': item.id, 'name': item.name} for item in items]), 200


if __name__ == '__main__':
    app.run(debug=True)
