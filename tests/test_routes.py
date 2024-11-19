def test_get_empty_pantry(client):
    """
    Test GET /pantry when the pantry is empty.
    """
    response = client.get('/pantry/')
    assert response.status_code == 200
    assert response.json == []  # Should return an empty list

def test_add_item_to_pantry(client, sample_data):
    """
    Test POST /pantry to add an item.
    """
    response = client.post('/pantry/', json=sample_data[0])  # Add the first sample item
    assert response.status_code == 201
    assert response.json['name'] == 'Rice'
    assert response.json['quantity'] == 10

def test_get_pantry_with_items(client, sample_data):
    """
    Test GET /pantry when items exist.
    """
    # Add items to the pantry
    for item in sample_data:
        client.post('/pantry/', json=item)

    response = client.get('/pantry/')
    assert response.status_code == 200
    assert len(response.json) == 2  # Two items should exist
    assert response.json[0]['name'] == 'Rice'
    assert response.json[1]['name'] == 'Flour'

def test_delete_item_from_pantry(client, sample_data):
    """
    Test DELETE /pantry/<id> to remove an item.
    """
    # Add an item to delete
    client.post('/pantry/', json=sample_data[0])
    response = client.delete('/pantry/1')  # Assuming ID 1
    assert response.status_code == 200
    assert response.json['message'] == 'Item deleted'

    # Verify item is deleted
    response = client.get('/pantry/')
    assert response.json == []  # Pantry should now be empty

def test_preview_items(client):
    """
    Test the /preview-items endpoint to ensure it validates and returns data correctly.
    """
    # Mock form data sent to the preview endpoint
    response = client.post('/pantry/preview-items', data={
        'name[]': ['Rice', 'Flour'],
        'quantity[]': ['5', '10']
    })
    assert response.status_code == 200
    assert response.json['preview'] == [
        {'name': 'Rice', 'quantity': 5},
        {'name': 'Flour', 'quantity': 10}
    ]


def test_preview_items_invalid_input(client):
    """
    Test the /preview-items endpoint with invalid input to ensure it handles errors.
    """
    response = client.post('/pantry/preview-items', data={
        'name[]': ['Rice', ''],
        'quantity[]': ['5', '']
    })
    assert response.status_code == 400
    assert "error" in response.json


def test_save_items(client):
    """
    Test the /save-items endpoint to ensure valid data is saved to the database.
    """
    # Mock JSON payload sent to the save endpoint
    response = client.post('/pantry/save-items', json={
        'items': [
            {'name': 'Rice', 'quantity': 5},
            {'name': 'Flour', 'quantity': 10}
        ]
    })
    assert response.status_code == 201
    assert response.json['message'] == "Items saved successfully"

    # Verify items were saved to the database
    pantry_items = client.get('/pantry/').json
    assert len(pantry_items) == 2
    assert pantry_items[0]['name'] == 'Rice'
    assert pantry_items[1]['name'] == 'Flour'


def test_save_items_invalid_input(client):
    """
    Test the /save-items endpoint with invalid input to ensure it handles errors.
    """
    response = client.post('/pantry/save-items', json={})  # No items in payload
    assert response.status_code == 400
    assert "error" in response.json
