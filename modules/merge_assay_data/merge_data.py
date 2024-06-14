import pandas as pd


def operate(data_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:

    merged = pd.concat(data_dict, axis= 1)

    return merged


def main(data):

    processed_data = operate(data)

    return processed_data