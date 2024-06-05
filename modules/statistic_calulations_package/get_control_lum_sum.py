import pandas as pd
import numpy as np

global key_of_data_to_access
key_of_data_to_access = 'prepped_data'

#Function declarations
def calc_sums(df):
    return df.groupby(['Plate_and_Date','Control State']).sum()

def into_pivot_table(df):
    return df.pivot_table(
    index='Plate_and_Date', columns='Control State', values='activity_level', fill_value=0
    )

def relabel_columns(df):    
    df.columns = ['sum_activity_level_' + col[:3] for col in df.columns]


def operate(df):

    #GET THE SUM OF LUM PER CONTROL STATE PER PLATE#
    needed_columns = df [['Plate_and_Date', 'Control State', 'activity_level' ]]

    #group by plate then by control then calculate LUM sum of each group
    sums_calculated = calc_sums(needed_columns)

    #create pivot table to add calculated data as sepereate columns
    converted_to_pivot_table = into_pivot_table(sums_calculated)

    #Relabel columns
    #This function does not return anything
    relabel_columns(converted_to_pivot_table)

    return converted_to_pivot_table

def main(data):

    for key in data:

        associated_data = data[key]

        dataframe = associated_data[key_of_data_to_access]

        processed_data =  operate(dataframe)

        associated_data['control_state_sums'] = processed_data

    return data