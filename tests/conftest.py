import pytest
from app import app
from database import db
from pantry.models import PantryItem

@pytest.fixture
def test_app():
    """
    Create a test version of the Flask app with a separate test configuration.
    """
    app.config.from_object('config.TestingConfig')  # Use TestingConfig
    with app.app_context():
        db.create_all()  # Create tables for testing
        yield app  # Provide the app for tests
        db.drop_all()  # Clean up the database after tests

@pytest.fixture
def client(test_app):
    """
    Provides a test client for the Flask app.
    """
    return test_app.test_client()

@pytest.fixture
def sample_data():
    """
    Sample data for tests.
    """
    return [
        {'name': 'Rice', 'quantity': 10},
        {'name': 'Flour', 'quantity': 5},
    ]
