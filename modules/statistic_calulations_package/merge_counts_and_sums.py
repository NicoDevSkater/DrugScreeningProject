import pandas as pd

global sums_data_key, counts_data_key
sums_data_key = 'control_state_sums'
counts_data_key = 'control_state_counts'

#Function Declarations
def merge_counts_and_sums(df1,df2):
    return pd.merge(df1,df2, how="outer", on="Plate_and_Date")


def operate(counts, sums):

    # Merge the two DataFrames based on the common values in the "Plate_and_Date" column
    merged = merge_counts_and_sums(counts, sums)
    
    return merged


def main(data):

    for key in data:

        associated_data = data[key]

        sums_dataframe = associated_data[sums_data_key]
        counts_datafrane = associated_data[counts_data_key]

        processed_data =  operate(counts_datafrane,sums_dataframe)

        associated_data['counts_sums_merged'] = processed_data

        del associated_data[counts_data_key]
        del associated_data[sums_data_key]

    return data