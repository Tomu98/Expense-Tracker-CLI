import pytest
import csv
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def test_expenses():
    """Sample expense data for testing"""
    return [
        {"ID": "1", "Date": "2025-01-03", "Amount": "50.00", "Category": "Groceries", "Description": "Snacks with my sweetheart :)"},
        {"ID": "2", "Date": "2025-01-05", "Amount": "30.00", "Category": "Others", "Description": "Hanging out with my brother"},
        {"ID": "3", "Date": "2025-01-06", "Amount": "100.00", "Category": "Leisure", "Description": "I reserved GTA6"},
        {"ID": "4", "Date": "2025-01-07", "Amount": "20.00", "Category": "Others", "Description": "A gift for my mom"}
    ]


@pytest.fixture
def test_file_path(tmp_path, test_expenses):
    """Create and manage the test environment with a temporary expenses file"""
    # Crear directorio de datos
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()

    # Crear archivo de gastos
    file_path = data_dir / "expenses.csv"
    fieldnames = ["ID", "Date", "Amount", "Category", "Description"]

    # Inicializar archivo con datos de prueba
    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(test_expenses)
    
    return file_path
