import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data_loader import load_data

class TestDataLoader(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        # Mocking pandas.read_csv to return a sample DataFrame
        mock_read_csv.return_value = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': [4, 5, 6]
        })
        df = load_data('data/trades.csv')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 3)
        self.assertIn('Column1', df.columns)
        self.assertIn('Column2', df.columns)

    @patch('pandas.read_csv')
    def test_load_data_with_numeric_columns(self, mock_read_csv):
        # Mocking pandas.read_csv to return a sample DataFrame
        mock_read_csv.return_value = pd.DataFrame({
            'NumericColumn': ['10', '20', 'invalid'],
            'OtherColumn': ['A', 'B', 'C']
        })
        df = load_data('data/trades.csv', numeric_columns=['NumericColumn'])
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        self.assertEqual(df['NumericColumn'].dtype, 'float64')
        self.assertEqual(df['NumericColumn'].tolist(), [10.0, 20.0, 0.0])

    @patch('pandas.read_csv')
    def test_load_data_empty_file(self, mock_read_csv):
        # Mocking pandas.read_csv to return an empty DataFrame
        mock_read_csv.return_value = pd.DataFrame()
        df = load_data('data/empty_file.csv')
        self.assertIsNotNone(df)
        self.assertTrue(df.empty)

    @patch('pandas.read_csv')
    def test_load_data_invalid_file(self, mock_read_csv):
        # Mocking pandas.read_csv to raise a FileNotFoundError
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        with self.assertRaises(FileNotFoundError):
            load_data('data/non_existent_file.csv')

if __name__ == '__main__':
    unittest.main()