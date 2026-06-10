import pandas as pd

def load_data(file):
    name = file.name.lower()

    if name.endswith('.csv'):
        return pd.read_csv(file)

    elif name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format")