import pandas as pd
import numpy as np
import math


global key_of_data_to_access
key_of_data_to_access = 'prepped_data'

#Functions declarations

def control_counts_grouped_format(df):
        return df.groupby(['Plate_and_Date', 'Control State',]).size().reset_index(name='Count')

def turn_to_pivot_table(df):
        return df.pivot_table(index=['Plate_and_Date'], columns='Control State', values='Count', fill_value=0)

def relabel_columns(df):
        df.columns = ['total_' + col[:3] for col in df.columns]

def calculate_total_wells(df):
        df['total_wells'] = df["total_pos"] + df["total_neg"] + df["total_com"] + df["total_uns"]


def operate(df):

        #subsett to needed columns
        plate_date_and_control_state_columns = df[['Plate_and_Date','Control State']]

        #NUMBER OF POSITIVE/NEGATIVE/UNSPECIFIED CONTROLS AND COMPOUNDS PER PLATE#

        # Group by Plate and Control State, then count occurrences
        control_counts_per_plate = control_counts_grouped_format(plate_date_and_control_state_columns)

        # Pivot the table to make Control State values as columns
        converted_to_pivot_table = turn_to_pivot_table(control_counts_per_plate)

        #The last two functions don't return anything

        # Add "total_" to the beginning of each column name and abbreviate
        relabel_columns(converted_to_pivot_table)
        #GET THE SUM OF THE LAST FOUR COLUMNS#
        calculate_total_wells(converted_to_pivot_table)

        return converted_to_pivot_table


def main(data):

        for key in data:
        
                associated_data = data[key]

                dataframe = associated_data[key_of_data_to_access]

                processed_data =  operate(dataframe)

                associated_data['control_state_counts'] = processed_data

        return data
