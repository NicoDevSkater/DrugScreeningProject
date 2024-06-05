import pandas as pd
import numpy as np
global key_of_summarized_data, key_of_prepped_data
key_of_summarized_data = 'summary_table'
key_of_prepped_data = 'prepped_data'

def operate(summary_df, prepped_df):
    
    summary_df.reset_index(inplace=True)

    plate_date_column = prepped_df['Plate_and_Date']

    prepped_df['Plate'] = plate_date_column.apply(lambda str:int(str.split(' ')[0]))
    prepped_df['Run Date'] = plate_date_column.apply(lambda str:pd.to_datetime(str.split(' ')[1]))

    prepped_df.drop(columns='Plate_and_Date',inplace=True)
    
    prepped_df_only_compounds = prepped_df[prepped_df['Control State'] == 'compound']
    summary_df_only_compounds = summary_df[summary_df['Molecule Name'].notna()]

    merged =  pd.merge(summary_df_only_compounds, prepped_df_only_compounds, on=['Molecule Name', 'Structure (CXSMILES)', 'Plate', 'Run Date','Well'])

    return merged
    

def main(data):

    for key in data:

        associated_data = data[key]

        summary_data = associated_data[key_of_summarized_data]
        prepped_data = associated_data[key_of_prepped_data]

        processed_data = operate(summary_data, prepped_data)

        associated_data['compare_with_cdd_exports'] = processed_data

    return data
