from pantry.models import PantryItem

def test_create_pantry_item():
    """
    Test creation of a PantryItem model instance.
    """
    item = PantryItem(name="Sugar", quantity=15)
    assert item.name == "Sugar"
    assert item.quantity == 15

def test_pantry_item_to_dict():
    """
    Test the to_dict() method of PantryItem.
    """
    item = PantryItem(id=1, name="Sugar", quantity=15)
    item_dict = item.to_dict()
    assert item_dict == {"id": 1, "name": "Sugar", "quantity": 15}
