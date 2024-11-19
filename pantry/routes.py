from flask import Blueprint, request, jsonify
from .models import db, PantryItem

pantry_blueprint = Blueprint('pantry', __name__)

@pantry_blueprint.route('/', methods=['GET'])
def get_items():
    items = PantryItem.query.all()
    return jsonify([item.to_dict() for item in items])

@pantry_blueprint.route('/', methods=['POST'])
def add_item():
    data = request.json
    new_item = PantryItem(name=data['name'], quantity=data['quantity'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@pantry_blueprint.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = PantryItem.query.get_or_404(item_id)
    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify(item.to_dict())

@pantry_blueprint.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = PantryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204
