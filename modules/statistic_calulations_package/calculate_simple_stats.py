import pandas as pd


global key_of_data_to_access
key_of_data_to_access = 'prepped_data'

def operate(df):
     
    grouped = df.groupby(['Plate_and_Date', 'Control State'])

    stats_calculated = grouped.agg({'activity_level' : ['sum','mean','std','size']})

    print(stats_calculated)


def main(data):
    
    for key in data:
        
        associated_data = data[key]

        dataframe = associated_data[key_of_data_to_access]

        processed_data =  operate(dataframe)

        associated_data['control_state_counts'] = processed_data

    return data