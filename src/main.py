from summary import process_trades_data

def main():
    performance_summary_path = './data/performance_summary.csv'
    trades_path = './data/trades.csv'
    open_positions_path = './data/open_positions.csv'

    # Process the trades data and generate the report
    report_df = process_trades_data(performance_summary_path, open_positions_path, trades_path)
    print(report_df)

    # Save the report to a local CSV file
    output_path = './tmp/trades_report.csv'
    report_df.to_csv(output_path, index=False)
    print(f"Report saved to {output_path}")

if __name__ == '__main__':
    main()
