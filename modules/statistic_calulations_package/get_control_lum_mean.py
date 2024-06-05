import pandas as pd

global key_of_counts_and_sums_merged
key_of_counts_and_sums_merged = 'counts_sums_merged'

#Function declarations
def calculate_lum_mean_per_control(df):
    control_states = ["com", "neg", "pos", "uns"]
    for control_state in control_states:
        total_label = 'total_' + control_state
        sum_label = 'sum_activity_level_' + control_state
        
        # Calculate mean
        mean_label = 'mean_activity_level_' + control_state
        df[mean_label] = df[sum_label] / df[total_label]


def replace_NAN_with_zero(df):
    df.fillna(value=0,inplace=True)


def operate(df):

    #GET MEAN OF LUM PER CONTROL and COMPOUNDS PER PLATE#

    #These next two function do not return anything
    calculate_lum_mean_per_control(df)

    #Replace "NA" values with "0"
    replace_NAN_with_zero(df)

    return df

def main(data):

    for key in data:

        associated_data = data[key]

        dataframe = associated_data[key_of_counts_and_sums_merged]

        processed_data = operate(dataframe)

        associated_data['control_state_stats'] = processed_data

        del associated_data[key_of_counts_and_sums_merged]

    return data