def validate_item_data(data):
    if not data.get('name') or not isinstance(data['quantity'], int):
        raise ValueError("Invalid item data")
