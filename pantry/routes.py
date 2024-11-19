from flask import Blueprint, request, jsonify
from pantry.models import PantryItem
from pantry.utils import write_to_csv
import logging
import os
import csv  # Ensure this is imported for CSV handling
from database import db

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create the blueprint for pantry-related routes
pantry_blueprint = Blueprint('pantry', __name__)

# Route for GET and POST requests on `/pantry`
@pantry_blueprint.route('', methods=['GET', 'POST'])
@pantry_blueprint.route('/', methods=['GET', 'POST'])
def pantry():
    """
    Handles retrieving and adding pantry items.
    """
    if request.method == 'GET':
        # Fetch all pantry items
        items = PantryItem.query.all()
        pantry_data = [item.to_dict() for item in items]
        return jsonify(pantry_data)

    elif request.method == 'POST':
        # Add a new pantry item
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
    """
    Deletes a pantry item by ID.
    """
    item = db.session.get(PantryItem, id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404


@pantry_blueprint.route('/preview-items', methods=['POST'])
def preview_items():
    """
    Handles previewing items from form data.
    """
    try:
        form_data = request.form
        names = form_data.getlist('name[]')
        quantities = form_data.getlist('quantity[]')

        if not names or not quantities:
            return jsonify({"error": "Names and quantities are required"}), 400

        if len(names) != len(quantities):
            return jsonify({"error": "Mismatch in names and quantities"}), 400

        preview_data = []
        for name, quantity in zip(names, quantities):
            if not name or not quantity.isdigit():
                return jsonify({"error": f"Invalid input: {name}, {quantity}"}), 400
            preview_data.append({"name": name, "quantity": int(quantity)})

        return jsonify({"preview": preview_data}), 200
    except Exception as e:
        logging.error(f"Error in preview-items: {e}")
        return jsonify({"error": "Failed to preview items"}), 500


@pantry_blueprint.route('/save-items', methods=['POST'])
def save_items():
    """
    Saves verified items to the database from JSON payload.
    """
    try:
        data = request.get_json()
        items = data.get('items', [])

        if not items:
            return jsonify({"error": "No items to save"}), 400

        for item in items:
            new_item = PantryItem(name=item['name'], quantity=item['quantity'])
            db.session.add(new_item)

        db.session.commit()
        return jsonify({"message": "Items saved successfully"}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in save-items: {e}")
        return jsonify({"error": "Failed to save items"}), 500


@pantry_blueprint.route('/csv-preview', methods=['GET'])
def csv_preview():
    """
    Returns the contents of the parsed CSV file for user verification.
    """
    try:
        with open("parsed_receipt.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        return jsonify({"preview": data}), 200
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        logging.error(f"Error in csv-preview: {e}")
        return jsonify({"error": "Failed to read CSV"}), 500


@pantry_blueprint.route('/save-from-csv', methods=['POST'])
def save_from_csv():
    """
    Saves verified CSV data into the database.
    """
    try:
        with open("parsed_receipt.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_item = PantryItem(name=row['name'], quantity=int(row['quantity']))
                db.session.add(new_item)
            db.session.commit()
        return jsonify({"message": "Items saved to database"}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in save-from-csv: {e}")
        return jsonify({"error": "Failed to save items"}), 500


@pantry_blueprint.route('/upload-receipt', methods=['POST'])
def upload_receipt():
    """
    Handles receipt upload and writes mock data to a CSV for now.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    receipt_file = request.files['file']
    file_path = os.path.join("uploads", receipt_file.filename)
    receipt_file.save(file_path)

    # Mock parsing for now, replace with LLM later
    parsed_data = [{"name": "Rice", "quantity": 5}, {"name": "Flour", "quantity": 2}]

    try:
        write_to_csv(parsed_data)
        return jsonify({"message": "Receipt processed successfully", "csv": "parsed_receipt.csv"}), 200
    except Exception as e:
        logging.error(f"Error in upload-receipt: {e}")
        return jsonify({"error": "Failed to process receipt"}), 500
