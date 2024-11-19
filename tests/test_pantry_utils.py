import csv
import pytest
from pantry.utils import write_to_csv

@pytest.fixture
def test_write_to_csv(tmp_path):
    """
    Test `write_to_csv` to ensure it writes data correctly to a CSV file.
    """
    data = [
        {"name": "Rice", "quantity": 2, "price": 5.99},
        {"name": "Flour", "quantity": 1, "price": 2.49}
    ]
    csv_path = tmp_path / "test_receipt.csv"

    # Write data to CSV
    write_to_csv(data, csv_path)

    # Verify the contents of the CSV file
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    assert len(rows) == len(data), "Number of rows in CSV should match input data."
    for i, row in enumerate(rows):
        assert row['name'] == data[i]['name'], f"Row {i} 'name' field mismatch."
        assert int(row['quantity']) == data[i]['quantity'], f"Row {i} 'quantity' field mismatch."
        assert float(row['price']) == data[i]['price'], f"Row {i} 'price' field mismatch."


def test_write_to_csv_invalid_data(tmp_path):
    """
    Test `write_to_csv` with invalid data.
    """
    invalid_data = "This is not a list of dictionaries"
    csv_path = tmp_path / "invalid_test_receipt.csv"

    # Attempt to write invalid data to CSV
    with pytest.raises(ValueError, match="Invalid data provided for CSV writing."):
        write_to_csv(invalid_data, csv_path)


def test_write_to_csv_no_data(tmp_path):
    """
    Test `write_to_csv` with no data.
    """
    csv_path = tmp_path / "empty_test_receipt.csv"

    # Assert that a ValueError is raised for no data
    with pytest.raises(ValueError, match="Invalid data provided for CSV writing."):
        write_to_csv([], csv_path)


def test_write_to_csv_permission_error(tmp_path):
    """
    Test `write_to_csv` to handle permission errors.
    """
    data = [
        {"name": "Rice", "quantity": 2, "price": 5.99},
        {"name": "Flour", "quantity": 1, "price": 2.49}
    ]
    csv_path = tmp_path / "protected_test_receipt.csv"

    # Create a protected file to simulate a permission error
    csv_path.touch(0o000)

    # Attempt to write to the protected file
    with pytest.raises(PermissionError):
        write_to_csv(data, csv_path)

    # Restore file permissions for cleanup
    csv_path.chmod(0o644)
