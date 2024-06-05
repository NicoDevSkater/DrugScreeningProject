import pandas as pd
from .get_control_lum_mean import replace_NAN_with_zero

global key_of_prepped_data, key_of_control_stats
key_of_prepped_data = 'prepped_data'
key_of_control_stats = 'control_state_stats'

#Function Declarations
def subset_to_id_control_and_lum(df):
    return df [['Plate_and_Date', 'Control State', 'activity_level' ]]

def calculate_lum_stdev_per_control(df_to_change, original_df):

    control_states = ["compound", "negative control", "positive control (hit)", "unspecified control"]

    for control_state in control_states:

        #save standard deviation column label
        std_label = 'stdev_activity_level_' + control_state[:3]

        # Filter original DataFrame by control state, then calculate standard deviation per plate
        std_values = original_df.loc[original_df['Control State'] == control_state].groupby('Plate_and_Date')['activity_level'].std(ddof=1)
        
        # Map standard deviation values back to the DataFrame based on the plate index
        df_to_change[std_label] = df_to_change.index.map(std_values)


def operate(statistics_df, prepped_data_df):

    #subset prepped data to needed columns
    prepped_data_needed_columns = prepped_data_df [['Plate_and_Date', 'Control State', 'activity_level' ]]

    #Calculate Standard Deviation of LUM per control per plate
    calculate_lum_stdev_per_control(statistics_df, prepped_data_needed_columns)
 
    replace_NAN_with_zero(statistics_df)

def main(data):

    for key in data:

        associated_data = data[key]

        control_stats_df = associated_data[key_of_control_stats]
        prepped_data_df = associated_data[key_of_prepped_data]
        
        operate(control_stats_df, prepped_data_df)

        #no need to return anything from main becasue orginal dataframe was transformed inplace and name fits data features
        # print(associated_data)

    return data