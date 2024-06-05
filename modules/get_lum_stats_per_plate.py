import pandas as pd

def get_lum_stats(dataframe, column, aggregate_functions):
    df_grouped = dataframe.groupby("Plate_and_Date")
    return df_grouped.agg({column:aggregate_functions})