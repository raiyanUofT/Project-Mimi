import csv
import logging

def validate_item_data(data):
    if not data.get('name') or not isinstance(data['quantity'], int):
        raise ValueError("Invalid item data")

logging.basicConfig(level=logging.DEBUG)

def write_to_csv(data, csv_path="parsed_receipt.csv"):
    """
    Writes data to a CSV file.

    Args:
        data (list of dict): The data to write to the CSV file. Each dictionary represents a row.
        csv_path (str): The file path for the CSV.

    Raises:
        ValueError: If the data is not a list of dictionaries.
        Exception: For general errors in writing the file.
    """
    try:
        if not data or not isinstance(data, list):
            raise ValueError("Invalid data provided for CSV writing.")

        with open(csv_path, 'w', newline='') as csvfile:
            # Dynamically infer fieldnames from the first dictionary in the data
            fieldnames = data[0].keys() if data else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)

        logging.info(f"CSV file successfully written to: {csv_path}")
    except ValueError as ve:
        logging.error(f"Validation error: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")
        raise
