import pandas as pd

def main(df, rows = None, columns = None):

    if rows is None and columns is None:
        return df
    elif rows is None:
        return df[columns]
    elif columns is None:
        return df.loc[rows]
    else:
        return df.loc[rows, columns]
