import pandas as pd
from data_loader import load_data


def initial_data_summary(performance_summary):
    # Filter performance summary for stocks
    stocks_summary = performance_summary[performance_summary['Asset Category'] == 'Stocks']

    # Initialize a dictionary to hold initial quantities and prices
    initial_data = {}
    for _, row in stocks_summary.iterrows():
        symbol = row['Symbol']
        initial_data[symbol] = {
            'initial_quantity': row['Prior Quantity'],
            'initial_price': row['Prior Price'],
            'initial_values': -1 * row['Prior Quantity'] * row['Prior Price'],
        }
    return initial_data


def open_positions_summary(open_positions, initial_data):
    for symbol in initial_data.keys():
        symbol_data = open_positions[open_positions['Symbol'] == symbol]
        if not symbol_data.empty:
            initial_data[symbol]['open_position'] = {
                'quantity': symbol_data['Quantity'].mean(),
                'cost_basis': symbol_data['Cost Basis'].mean(),
                'cost_price': symbol_data['Cost Price'].mean(),
                'close_price': symbol_data['Close Price'].mean(),
                'value': symbol_data['Value'].mean()
            }
    return initial_data


def trade_data_summary(trades_data, symbols):
    # Filter trades data for stocks
    stocks_trades = trades_data[(trades_data['Asset Category'] == 'Stocks') & (
        trades_data['Header'] == 'Data')]

    # Initialize a dictionary to hold trades data
    trades_summary = {}

    for symbol in symbols:
        symbol_trades = stocks_trades[stocks_trades['Symbol'] == symbol]

        sum_quantity = symbol_trades['Quantity'].sum()
        sum_proceeds = symbol_trades['Proceeds'].sum()
        sum_comm_fee = symbol_trades['Comm/Fee'].sum()

        trades_summary[symbol] = {
            'total_buy': symbol_trades[symbol_trades['Proceeds'] < 0]['Proceeds'].sum(),
            'total_buy_quantity': symbol_trades[symbol_trades['Proceeds'] < 0]['Quantity'].sum(),
            'total_sell': symbol_trades[symbol_trades['Proceeds'] > 0]['Proceeds'].sum(),
            'total_sell_quantity': symbol_trades[symbol_trades['Proceeds'] > 0]['Quantity'].sum(),
            'sum_quantity': sum_quantity,
            'sum_proceeds': sum_proceeds,
            'sum_comm_fee': sum_comm_fee
        }
    return trades_summary


def process_trades_data(trades_activity_path_path, type_configs):
    trades_activity = load_data(trades_activity_path_path, type_configs)
    initial_summary = initial_data_summary(
        trades_activity['performance_summary'])
    initial_summary = open_positions_summary(
        trades_activity['open_positions'], initial_summary)
    trades_summary = trade_data_summary(
        trades_activity['trades'], initial_summary.keys())

    # Validate final quantities
    trades_tax_resutls = []

    for symbol, init_data in initial_summary.items():
        trade_data = trades_summary[symbol]

        initial_quantity = init_data['initial_quantity']
        final_quantity = initial_quantity + trade_data['sum_quantity']
        open_position_value = final_quantity * \
            init_data.get('open_position', {}).get('cost_price', 0)
        total_tax_buy = init_data['initial_values'] + \
            trade_data['total_buy'] + open_position_value
        total_sell = trade_data['total_sell']

        trades_tax_resutls.append({
            'symbol': symbol,
            'initial_quantity': initial_quantity,
            'buy_quantity': trade_data['total_buy_quantity'],
            'final_quantity': final_quantity,
            'total_tax_sell': round(total_sell, 2),
            'total_tax_buy': round(abs(total_tax_buy), 2),
            'trade_comm_fee': round(abs(trade_data['sum_comm_fee']), 2),
            'total_gain_loss': round(total_sell + total_tax_buy + trade_data['sum_comm_fee'], 2),
            'open_position_value': round(abs(open_position_value), 2),
            'current_values': init_data.get('open_position', {}).get('value', 0)
        })

    return pd.DataFrame(trades_tax_resutls)


def currency_convert(report_df, rate, ignore_columns=['symbol', 'initial_quantity', 'buy_quantity', 'final_quantity']):
    """
    Converts all numeric fields in the table to a different currency using the given rate,
    excluding the 'symbol' and 'quantity' fields.

    Args:
        rate (float): Conversion rate to apply.
        table (pd.DataFrame): DataFrame containing the data to convert.
        ignore_columns: (list): List of columns to ignore during conversion.

    Returns:
        pd.DataFrame: DataFrame with converted values.
    """
    # Identify columns to convert (exclude 'symbol' and 'quantity')
    columns_to_convert = [
        col for col in report_df.columns if col not in ignore_columns]

    # Apply conversion to the selected columns
    df_converted = report_df.copy()
    for col in columns_to_convert:
        if pd.api.types.is_numeric_dtype(df_converted[col]):
            df_converted[col] = round(df_converted[col] * rate, 2)

    return df_converted
