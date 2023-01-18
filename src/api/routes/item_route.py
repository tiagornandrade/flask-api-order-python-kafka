
from flask import Blueprint, jsonify, request
from uuid import uuid4
import database.item_sql as sql

item_route = Blueprint('item', __name__, url_prefix='/item')

@item_route.route('/list/', methods=['GET'])
def list_user():
    user_list = sql.list_user()
    return jsonify(user_list), 200

@item_route.route('/create/', methods=['PUT'])
def create_item():
    item = request.json
    item['id'] = str(uuid4())   
    sql.save_item(item)
    return jsonify(item), 201

@item_route.route('/find/', methods=['GET'])
def find_user():
    name = request.args.get('name')
    founded = sql.find_by_name(name)
    return jsonify(founded), 200

@item_route.route('/<uuid>/', methods=['DELETE'])
def delete_user(uuid):
    sql.delete(uuid)
    return jsonify({'message': 'User removed'}), 200