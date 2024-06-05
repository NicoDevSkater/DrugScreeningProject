import pandas as pd

global key_of_prepped_data, key_of_outlier_status, key_of_stats_per_plate
key_of_prepped_data = 'prepped_data'
key_of_outlier_status = 'control_points_outlier_status'
key_of_stats_per_plate = 'stats_per_plate'



def operate(prepped_data_df, outlier_status_df):
    
    #First filter the outlier_status_df to only include rows that are 'non_outlier'
    
    outliers_only = outlier_status_df[outlier_status_df['is_outlier'] != 'non_outlier']

    # Ensure the columns 'Plate_and_Date', 'Control State', 'activity_level', and 'Well' are present in both datasets
    key_columns = ['Plate_and_Date', 'Control State', 'activity_level', 'Well']

    # Merge the main dataset with the outliers dataset on the key columns to identify rows to remove
    merged_df = pd.merge(prepped_data_df, outliers_only[key_columns], on=key_columns, how='left', indicator=True)

    # Filter out the rows that are identified as outliers (present in both datasets)
    filtered_df = merged_df[merged_df['_merge'] == 'left_only']

    # Drop the '_merge' column as it is no longer needed
    filtered_df.drop(columns=['_merge'], inplace=True)

    # Return the filtered dataset
    return filtered_df
def main(data):

    for key in data:

        associated_data = data[key]
        #Make copy of data to packege
        associated_data_copy = associated_data.copy()
        #Assign copy to property
        associated_data['conditions_before_recalculations'] = associated_data_copy
        #delete orignal properties
        del associated_data[key_of_prepped_data]

        del associated_data[key_of_outlier_status]

        del associated_data[key_of_stats_per_plate]

        prev_conditions = associated_data['conditions_before_recalculations']

        prepped_data = prev_conditions[key_of_prepped_data]

        outlier_data = prev_conditions[key_of_outlier_status]

        processed_data = operate(prepped_data, outlier_data)

        associated_data['prepped_data'] = processed_data
    
    return data