from summary import process_trades_data
import os
import argparse

type_configs = {
    'performance_summary': {
        "type_pattern": 'Mark-to-Market Performance Summary',
        "numeric_columns": ['Prior Quantity', 'Prior Price', 'Current Quantity', 'Current Price'],
    },
    'open_positions': {
        "type_pattern": 'Open Positions',
        "numeric_columns": ['Quantity', 'Cost Basis', "Cost Price", "Close Price", "Value"],
    },
    'trades': {
        "type_pattern": 'Trades',
        "numeric_columns": ['Quantity', 'Proceeds', 'Comm/Fee'],
    }
}

def main():
    parser = argparse.ArgumentParser(description='Process trades data and generate a tax report.')
    parser.add_argument('--file', type=str, default='./data/test.csv',
                        help='Path to the trades activity CSV file.')
    args = parser.parse_args()
    
    trades_activity_file_path = args.file

    if not os.path.exists(trades_activity_file_path):
        print(f"Error: File not found at {trades_activity_file_path}")
        return

    # Process the trades data and generate the report
    report_df = process_trades_data(trades_activity_file_path, type_configs)
    print(report_df)

    # Save the report to a local CSV file
    output_path = './tmp/trades_tax_report.csv'
    report_df.to_csv(output_path, index=False)
    print(f"Report saved to {output_path}")

if __name__ == '__main__':
    main()
