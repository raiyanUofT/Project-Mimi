from flask import Blueprint, request, jsonify
from pantry.models import PantryItem
from database import db
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the blueprint for pantry-related routes
pantry_blueprint = Blueprint('pantry', __name__)

# Route for GET and POST requests on `/pantry`
@pantry_blueprint.route('', methods=['GET', 'POST'])  # No trailing slash
@pantry_blueprint.route('/', methods=['GET', 'POST'])  # With trailing slash
def pantry():
    if request.method == 'GET':
        items = PantryItem.query.all()
        pantry_data = [item.to_dict() for item in items]
        return jsonify(pantry_data)

    elif request.method == 'POST':
        try:
            new_item_data = request.get_json()
            logging.debug(f"Received POST data: {new_item_data}")
            new_item = PantryItem(name=new_item_data['name'], quantity=new_item_data['quantity'])
            db.session.add(new_item)
            db.session.commit()
            logging.debug(f"Added new item to database: {new_item.to_dict()}")
            return jsonify(new_item.to_dict()), 201
        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            return jsonify({"error": "Failed to add item"}), 500

# Route for deleting a pantry item by ID
@pantry_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = PantryItem.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404
