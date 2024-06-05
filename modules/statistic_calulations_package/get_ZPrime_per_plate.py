import pandas as pd

global key_of_control_state_stats
key_of_control_state_stats = 'control_state_stats'

def calculate_z_prime(df):
    
    positive_mean = df['mean_activity_level_pos']
    negative_mean = df['mean_activity_level_neg']
    positive_std = df['stdev_activity_level_pos']
    negative_std = df['stdev_activity_level_neg']
    
    # Calculate Z' prime value | This equation is done on every single row
    df['Z_prime'] = 1 - ((3 * positive_std) + (3 * negative_std)) / abs(positive_mean - negative_mean)


def operate(df):

    # Calculate the mean and standard deviation for positive and negative controls
    #This function does not return anything
    calculate_z_prime(df)

    return df

def main(data):

    for key in data:

        associated_data = data[key]

        dataframe = associated_data[key_of_control_state_stats]

        #Not need to return anything from main, operations were done inplace
        processed_data = operate(dataframe)

        associated_data['stats_per_plate'] = processed_data

        del associated_data[key_of_control_state_stats]

    return data