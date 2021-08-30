import pandas as pd

def get_dataset(url='dataset.xlsx'):
    return pd.read_excel(url)
