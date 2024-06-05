import pandas as pd

global key_of_data_to_access
key_of_data_to_access = 'stats_per_plate'

"""
The coefficient of variation needs to be calculated in order to identify error plates that need inspection
Indentifying these plates allows us to compensate for the possible errors to improve statistical accuraccy in downstream compound testing and investigation
"""

#Function declarations
def add_coefficient_of_variation_columns(df):
    df["Coefficient_Variation_neg"] = df["stdev_activity_level_neg"] / df["mean_activity_level_neg"]
    df["Coefficient_Variation_pos"] = df["stdev_activity_level_pos"] / df["mean_activity_level_pos"]

def add_max_min_coefficient_of_variation_columns(df):
    
    df["max_Coefficient_Variation"] = df[["Coefficient_Variation_neg", "Coefficient_Variation_pos"]].max(axis=1)
    df["min_Coefficient_Variation"] = df[["Coefficient_Variation_neg", "Coefficient_Variation_pos"]].min(axis=1)


def operate(df):

    add_coefficient_of_variation_columns(df)

    # Find the maximum and minimum value between the two columns for each row
    add_max_min_coefficient_of_variation_columns(df)


def main(data):

    for key in data:

        associated_data = data[key]

        dataframe = associated_data[key_of_data_to_access]

        operate(dataframe)

    return data