import csv
import logging

logging.basicConfig(level=logging.DEBUG)

def parse_receipt(file_path):
    """
    Parses a receipt file and returns data as a list of dictionaries.
    For now, this uses mock data but can be replaced with LLM or OCR integration.
    """
    try:
        # Mock parsed data
        parsed_data = [
            {'name': 'Rice', 'quantity': 2, 'price': 5.99},
            {'name': 'Flour', 'quantity': 1, 'price': 2.49}
        ]
        logging.info(f"Parsed data from receipt: {parsed_data}")
        return parsed_data
    except Exception as e:
        logging.error(f"Error parsing receipt: {e}")
        return []
