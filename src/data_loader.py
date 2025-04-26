import pandas as pd
import csv

# type_configs = {
#     'performance_summary': {
#         "type_pattern": 'Mark-to-Market Performance Summary',
#         "numeric_columns": ['Prior Quantity', 'Prior Price', 'Current Quantity', 'Current Price'],
#     },
#     'open_positions': {
#         "type_pattern": 'Open Positions',
#         "numeric_columns": ['Quantity', 'Cost Basis', "Cost Price", "Close Price", "Value"],
#     },
#     'trades': {
#         "type_pattern": 'Trades',
#         "numeric_columns": ['Quantity', 'Proceeds', 'Comm/Fee'],
#     }
# }


def load_data(file_path, type_configs):
    """
    Loads data from a CSV file where the first row of each type specifies column names.

    Args:
        file_path (str): Path to the CSV file.
        type_configs (dict): Dictionary mapping row type field name to starting patterns (strings) 
                            and List of column names to convert to numeric.

    Returns:
        dict: Dictionary containing pandas DataFrames for each row type.
    """
    data = {}
    column_specs = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            line = ','.join(row)
            matched_type = None
            for type_name, pattern in type_configs.items():
                if line.startswith(pattern['type_pattern']):
                    matched_type = type_name
                    break

            if matched_type:
                if matched_type not in data:
                    # First row of this type, treat as column names
                    column_specs[matched_type] = row
                    data[matched_type] = []  # Initialize data list
                else:
                    column_names = column_specs[matched_type]
                    values = row  # Use the current row's values
                    if len(values) < len(column_names):
                        values += [''] * (len(column_names) - len(values))
                    elif len(values) > len(column_names):
                        values = values[:len(column_names)]
                    row_data = dict(zip(column_names, values))
                    data[matched_type].append(row_data)

    # Convert lists of dictionaries to pandas DataFrames
    dfs = {}
    for type_name, rows in data.items():
        numeric_columns = type_configs[type_name].get('numeric_columns', [])
        df = pd.DataFrame(rows)
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        dfs[type_name] = df

    return dfs
