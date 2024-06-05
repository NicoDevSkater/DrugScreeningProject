import pandas as pd
import numpy as np
from .load_raw_data import screening_data_mapped


"""
Some plates had a really low z-score on their first run
These plates were run a second time so there will be some duplicate measurements in the dataset
The re-runs most likely took place on a seperate data so a new column will be added to each dataset
This column will be used to indentify duplicates from  eachother

I want drop empty columns "Obs CatNumb ORFEOME" will always be an empty column

I will also end up dropping the orginal "Plate" and "Run Date" columns

The final tweak I want to make is specifying that empty rows in the control state column are compounds this
is solely for computing purposes and won't do nay good be ing shown to reviewers of tables
"""

global key_of_data_to_access
key_of_data_to_access = 'prepped_data'


def main(data):
    
    for key in data:
        associated_data = data[key]

        prepped_data = associated_data[key_of_data_to_access]

        combine_plate_and_rundate_columns(prepped_data)
        
        #Now drop empty columns
        prepped_data.dropna(how='all', axis = 1, inplace=True)

        #Assign each empty row in the "control state" column to the string "compound"
        prepped_data.fillna({'Control State':'compound'}, inplace=True)

        renamed_columns_dict = harmonize_activity_level_column(prepped_data)

        keys_values_inverted = {v: k for k, v in renamed_columns_dict.items()}
        
        associated_data['meta_data']['renamed_columns_mapped'] = keys_values_inverted
    
    return data

def harmonize_activity_level_column(df):

    #keep original columns name as metadata
    # original_activity_level_name = df.columns[5]
    df_columns = df.columns

    to_compare = [
        "Plate_and_Date","Well","Batch Name","Structure (CXSMILES)","Molecule Name","Control State"
        ]
    
    to_rename = list(set(df_columns) - set(to_compare))    

    renaming_dict = {}

    if len(to_rename) == 4:

        renaming_dict = {
            df_columns[5]:'activity_level',
            df_columns[6]: "z_prime_activity_level",
            df_columns[7]: "npi",
            df_columns[8]: "z_score_activity_level"
        }
    else: renaming_dict = {
            df_columns[5]:'activity_level',
            df_columns[6]: "z_prime_activity_level",
            df_columns[7]: "npi"
        }

   #rename the 6th column to "activity_level" (arrays are zero based)
    df.rename(columns=renaming_dict, inplace=True)

    return renaming_dict

def combine_plate_and_rundate_columns(dataframe):
    
    #Combine the two columns and seprate them by a space character
    dataframe["Plate_and_Date"] = dataframe['Plate'].astype(str) + ' ' + dataframe['Run Date'].astype(str)
    #drop the 'Plate' and "Run Date" column
    columns_to_drop = ['Plate','Run Date']
    dataframe.drop(columns=columns_to_drop, inplace=True)

    
prepped_data = main(screening_data_mapped)
