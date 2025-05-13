import unittest
from unittest.mock import patch
from utils.load import load_data
import sys
import io

class TestLoad(unittest.TestCase):

    @patch('utils.load.store_to_csv')
    @patch('utils.load.store_to_postgre')
    @patch('utils.load.dataframe_to_sheets')
    def test_load_data_success(self, mock_gsheets, mock_postgre, mock_csv):
        data = [{"Product Title": "Test Product", "Price": 1600000.0, "Rating": 4.5, "Colors": 10}]
        db_url = "postgresql://user:password@localhost:5432/mydatabase"
        sheet_name = "Test Sheet"
        gsheet_id = "123456789"

        # Call the load_data function
        load_data(data, db_url, sheet_name, gsheet_id)

        # Assert that each of the mocked functions was called once
        mock_csv.assert_called_once_with(data)
        mock_postgre.assert_called_once_with(data, db_url)
        mock_gsheets.assert_called_once_with(data, sheet_name, gsheet_id)

    @patch('utils.load.store_to_csv')
    @patch('utils.load.store_to_postgre')
    @patch('utils.load.dataframe_to_sheets')
    @patch('sys.stdout', new_callable=io.StringIO)  # Capture print output
    def test_load_data_failure(self, mock_stdout, mock_gsheets, mock_postgre, mock_csv):
        # Simulate an error in the CSV loading function
        mock_csv.side_effect = Exception("CSV Error")
        data = [{"Product Title": "Test Product", "Price": 1600000.0, "Rating": 4.5, "Colors": 10}]
        
        # Call the load_data function
        load_data(data, "db_url", "sheet_name", "gsheet_id")

        # Check if the error message is printed
        output = mock_stdout.getvalue()
        self.assertIn("Terjadi kesalahan saat memuat data: CSV Error", output)

if __name__ == '__main__':
    unittest.main()