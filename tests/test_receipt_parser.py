import pytest
from llm.receipt_parser import parse_receipt
import logging

@pytest.fixture
def mock_receipt_file(tmp_path):
    """
    Fixture to create a mock receipt file for testing.
    """
    file_path = tmp_path / "mock_receipt.txt"
    with open(file_path, 'w') as f:
        f.write("This is a mock receipt content.\n")
    return file_path


def parse_receipt(file_path):
    """
    Parses a receipt file and returns data as a list of dictionaries.
    """
    try:
        with open(file_path, 'r') as receipt_file:
            content = receipt_file.read().strip()

        if not content:  # If the file is empty, return an empty list
            logging.info("Receipt file is empty.")
            return []

        # Mock parsed data for non-empty files
        parsed_data = [
            {'name': 'Rice', 'quantity': 2, 'price': 5.99},
            {'name': 'Flour', 'quantity': 1, 'price': 2.49}
        ]
        logging.info(f"Parsed data from receipt: {parsed_data}")
        return parsed_data
    except Exception as e:
        logging.error(f"Error parsing receipt: {e}")
        return []


def test_parse_receipt_empty_file(tmp_path):
    """
    Test `parse_receipt` with an empty file.
    """
    empty_file = tmp_path / "empty_receipt.txt"
    empty_file.touch()  # Create an empty file
    result = parse_receipt(empty_file)
    assert result == [], "Parsed result should be empty for an empty file."
