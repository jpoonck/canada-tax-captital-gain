import pandas as pd
from data_loader import load_data

def initial_data_summary(performance_summary_path):
    performance_summary = load_data(performance_summary_path, numeric_columns=['Prior Quantity', 'Prior Price', 'Current Quantity', 'Current Price'])
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

def open_positions_summary(open_position_path, initial_data):
    open_positions = load_data(open_position_path, numeric_columns=['Quantity', 'Cost Basis', "Cost Price", "Close Price", "Value"])
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


def trade_data_summary(trades_path, symbols):
     # Load trades data
    trades_data = load_data(trades_path, numeric_columns=['Quantity', 'Proceeds', 'Comm/Fee'])
    stocks_trades = trades_data[(trades_data['Asset Category'] == 'Stocks') & (trades_data['Header'] == 'Data')]
    
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

def process_trades_data(performance_summary_path, open_positions_path, trades_path):
    initial_summary = initial_data_summary(performance_summary_path)
    initial_summary = open_positions_summary(open_positions_path, initial_summary)
    trades_summary = trade_data_summary(trades_path, initial_summary.keys())
    
    # Validate final quantities
    trade_report_resutls = []
    
    for symbol, init_data in initial_summary.items():
        trade_data = trades_summary[symbol]

        initial_quantity = init_data['initial_quantity']
        final_quantity = initial_quantity + trade_data['sum_quantity']
        open_position_value = final_quantity * init_data.get('open_position', {}).get('cost_price', 0)
        total_tax_buy = init_data['initial_values'] + trade_data['total_buy'] + open_position_value
        total_sell = trade_data['total_sell']
        
        trade_report_resutls.append({
            'symbol': symbol,
            'initial_quantity': initial_quantity,
            'buy_quantity': trade_data['total_buy_quantity'],
            'final_quantity': final_quantity,
            'total_tax_sell': "{:.2f}".format(total_sell),
            'total_tax_buy': "{:.2f}".format(abs(total_tax_buy)),
            'trade_comm_fee': "{:.2f}".format(abs(trade_data['sum_comm_fee'])),
            'total_gain_loss': "{:.2f}".format(total_sell + total_tax_buy + trade_data['sum_comm_fee']),
            'open_position_value': "{:.2f}".format(abs(open_position_value)),
            'current_values': init_data.get('open_position', {}).get('value', 0)
        })
    
    return pd.DataFrame(trade_report_resutls)