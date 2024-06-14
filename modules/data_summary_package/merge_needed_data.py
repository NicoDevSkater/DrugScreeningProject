import pandas as pd
import numpy as np
import os

global key_of_npi_stats, key_of_outlier_status, key_of_stats_per_plate, key_of_previous_conditions
key_of_npi_stats = 'npi_stats'
key_of_outlier_status = 'control_points_outlier_status'
key_of_previous_conditions = 'conditions_before_recalculations'
key_of_stats_per_plate = 'stats_per_plate'



def series_to_numpy(series):
    return series.tolist()




def operate(npi_df, outlier_df, stats_df, prev_stats_df):

    #Init new column in npi_df, default value is 'no' for all rows
    npi_df['has_outliers'] = 'no'

    unique_plate_and_date = npi_df.index.unique()

    for id in unique_plate_and_date:

        group_from_outliers_df = outlier_df[outlier_df['Plate_and_Date'] == id]

        group_from_npi_df = npi_df.loc[id]

        has_any_outliers = (group_from_outliers_df['is_outlier'] != 'non_outlier').any()
        
        if has_any_outliers:

            outliers = group_from_outliers_df[group_from_outliers_df['is_outlier'] != 'non_outlier']
            
            outliers['Control State Abbrev'] = outliers['Control State'].str[:3]

            outliers['outliers_described'] = outliers['Control State Abbrev'] +', '+ outliers['is_outlier']

            outlier_descriptions = ['; '.join(map(str,outliers['outliers_described']))] * len(group_from_npi_df['has_outliers'])

            npi_df.at[id, 'has_outliers'] = outlier_descriptions

    #Merge z prime per plate with npi_df
    npi_stats_with_z_prime = pd.merge(npi_df, stats_df, left_index=True, right_index=True)

    #Then merge th prev_Z_prime but rename it first so there is no conflict
    prev_stats_df['prev_Z_prime'] = prev_stats_df['Z_prime']
    prev_stats_df.drop('Z_prime', axis=1, inplace=True)
    npi_stats_with_prev_z_prime = pd.merge(npi_stats_with_z_prime, prev_stats_df, left_index=True, right_index=True)

    return npi_stats_with_prev_z_prime

def subset_to_needed_data(df, rows = None, columns = None):

    if rows is None and columns is None:
        return df
    elif rows is None:
        return df[columns]
    elif columns is None:
        return df.loc[rows]
    else:
        return df.loc[rows, columns]


def main(data):
    
    for key in data:

        associated_data = data[key]

        prev_conditions = associated_data[key_of_previous_conditions]

        npi_data = associated_data[key_of_npi_stats]

        stats_per_plate = associated_data[key_of_stats_per_plate]

        stats_per_plate_before_recalculation = prev_conditions[key_of_stats_per_plate]

        outlier_data = prev_conditions[key_of_outlier_status]

        stats_per_plate_needed_columns = ['Z_prime']
        prev_stats_per_plate_needed_columns = ['Z_prime']
        outlier_data_needed_columns = ['Plate_and_Date', 'Control State','is_outlier']

        
        stats_needed = subset_to_needed_data(stats_per_plate, columns = stats_per_plate_needed_columns)
        prev_stats_needed = subset_to_needed_data(stats_per_plate_before_recalculation, columns = prev_stats_per_plate_needed_columns)
        outlier_data_needed = subset_to_needed_data(outlier_data, columns = outlier_data_needed_columns)

        processed_data = operate(npi_data, outlier_data_needed, stats_needed, prev_stats_needed)

        #UPLOAD NPI PER COMPOUND AS CSV

        #subset to compounds only
        compounds_only = processed_data[processed_data['Control State'] == 'compound']

        #get directory to upload data
        path = os.getenv("NPI_PER_COM")

        compounds_rst_indx = compounds_only.reset_index()

        compounds_only.to_csv(path + 'npi-per-compound-' + key + '.csv')

        associated_data['summary_table'] = processed_data
    return data