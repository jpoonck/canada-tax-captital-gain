import unittest
import pandas as pd
from src.summary import (
    initial_data_summary,
    open_positions_summary,
    trade_data_summary,
    process_trades_data
)

class TestSummary(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.performance_summary_data = pd.DataFrame({
            'Asset Category': ['Stocks', 'Stocks', 'Bonds'],
            'Symbol': ['AAPL', 'GOOG', 'BND'],
            'Prior Quantity': [10, 20, 30],
            'Prior Price': [150, 2500, 100],
            'Current Quantity': [15, 25, 35],
            'Current Price': [155, 2600, 105]
        })

        self.open_positions_data = pd.DataFrame({
            'Symbol': ['AAPL', 'GOOG', 'BND'],
            'Quantity': [5, 10, 15],
            'Cost Basis': [750, 25000, 1500],
            'Cost Price': [150, 2500, 100],
            'Close Price': [155, 2600, 105],
            'Value': [775, 26000, 1575]
        })

        self.trades_data = pd.DataFrame({
            'Asset Category': ['Stocks', 'Stocks', 'Stocks'],
            'Header': ['Data', 'Data', 'Data'],
            'Symbol': ['AAPL', 'GOOG', 'AAPL'],
            'Quantity': [5, -10, -5],
            'Proceeds': [750, -25000, -750],
            'Comm/Fee': [5, 10, 5]
        })

    def test_initial_data_summary(self):
        result = initial_data_summary(self.performance_summary_data)
        self.assertIn('AAPL', result)
        self.assertIn('GOOG', result)
        self.assertNotIn('BND', result)
        self.assertEqual(result['AAPL']['initial_quantity'], 10)
        self.assertEqual(result['AAPL']['initial_price'], 150)

    def test_open_positions_summary(self):
        initial_data = {
            'AAPL': {'initial_quantity': 10, 'initial_price': 150},
            'GOOG': {'initial_quantity': 20, 'initial_price': 2500}
        }
        result = open_positions_summary(self.open_positions_data, initial_data)
        self.assertIn('open_position', result['AAPL'])
        self.assertEqual(result['AAPL']['open_position']['quantity'], 5)
        self.assertEqual(result['AAPL']['open_position']['cost_basis'], 750)

    def test_trade_data_summary(self):
        symbols = ['AAPL', 'GOOG']
        result = trade_data_summary(self.trades_data, symbols)
        self.assertIn('AAPL', result)
        self.assertIn('GOOG', result)
        self.assertEqual(result['AAPL']['total_buy'], -750)
        self.assertEqual(result['AAPL']['total_sell'], 750)

    def test_process_trades_data(self):
        performance_summary_path = './data/performance_summary.csv'
        open_positions_path = './data/open_positions.csv'
        trades_path = './data/trades.csv'

        # Mocking the load_data function to return sample data
        pd.read_csv = lambda *args, **kwargs: {
            performance_summary_path: self.performance_summary_data,
            open_positions_path: self.open_positions_data,
            trades_path: self.trades_data
        }[args[0]]

        result = process_trades_data(performance_summary_path, open_positions_path, trades_path)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('symbol', result.columns)
        self.assertIn('total_gain_loss', result.columns)

if __name__ == '__main__':
    unittest.main()