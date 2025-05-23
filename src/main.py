from summary import process_trades_data, currency_convert
import os
import argparse

# Example conversion rate, usd to cad 2024, replace with actual rate
usd_to_cad_rate = 1.3698
default_file_path = './data/test.csv'
default_output_path = './tmp/trades_tax_report.csv'
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
    parser = argparse.ArgumentParser(
        description='Process trades data and generate a tax report.')
    parser.add_argument('--file', type=str, default=default_file_path,
                        help='Path to the trades activity CSV file.')
    parser.add_argument('--output', type=str, default=default_output_path,
                        help='Path to save the output report CSV file. Defaults to '+default_output_path)
    parser.add_argument('--rate', type=float, default=usd_to_cad_rate,
                        help='Exchange rate to convert report to target currency. Defaults to '+str(usd_to_cad_rate))
    args = parser.parse_args()

    trades_activity_file_path = args.file
    exchange_rate = args.rate
    output_path = args.output

    if not os.path.exists(trades_activity_file_path):
        print(f"Error: File not found at {trades_activity_file_path}")
        return

    # Process the trades data and generate the report
    report_df = process_trades_data(trades_activity_file_path, type_configs)
    print(report_df.head(50))

    # Save the report to a local CSV file
    report_df.to_csv(output_path, index=False)
    print(f"Report saved to {output_path}")

    if exchange_rate != 1:
        print("Converting report to CAD with rate: " + str(exchange_rate))
        report_df_cad = currency_convert(report_df, exchange_rate)
        print(report_df_cad.head(50))


if __name__ == '__main__':
    main()
