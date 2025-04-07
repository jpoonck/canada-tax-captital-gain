import pandas as pd

def load_data(file_path, numeric_columns=[]):
    # Read the CSV file
    df = pd.read_csv(file_path, header=0, delimiter=",", low_memory=False)
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# # Example usage
# file_path = './data/trades.csv'
# grouped_data = load_and_group_data(file_path)

# # Print the grouped data for verification
# for type_name, content in grouped_data.items():
#     print(f"Type Name: {type_name}")
#     print("Header:")
#     print(content['header'])
#     print("Data:")
#     print(content['data'])
#     print("\n")