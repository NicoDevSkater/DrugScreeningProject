import pandas as pd
import numpy as np


"""
Calculating the minimum and maximum z scores for the positive and negaive controls will allow us to tell how bad a plate is
From there we can decide what to do with the outliers amongst the controls

The Coefficient of variation for the entire group pe r plate must be plotted with each datapoints from negative and positive contorls

We need the prepped data as well to access each data point of a plate.

First filter to rows that are positive or negative control measurements
"""
global key_of_prepped_data, key_of_stats_per_plate
key_of_prepped_data = 'prepped_data'
key_of_stats_per_plate = 'stats_per_plate'

#Class Declarations
class Calculate_Z_Score_Per_Control:

    def __init__(self, statistics_dataframe):
        
        self.stats_df = statistics_dataframe

        self.pos_control_info = {
            'mean': np.nan,
            'stdev': np.nan
        }

        self.neg_control_info = {
            'mean': np.nan,
            'stdev': np.nan
        }


    def main(self, group_df):

        self.update_group_info(group_df)

        for index,row in group_df.iterrows():
            
            row_score = row['activity_level']

            if row['Control State'] == 'positive control (hit)':
            
                row_z_score = self.calc_z_score(row_score, self.pos_control_info)

                group_df.loc[index, 'z_score'] = row_z_score
                
            elif row['Control State'] == 'negative control':
                
                row_z_score = self.calc_z_score(row_score, self.neg_control_info)

                group_df.loc[index, 'z_score'] = row_z_score
        
        #Drop Plate_and_Date column before returning
        group_df.drop(columns='Plate_and_Date', inplace=True)
        return group_df

    def update_group_info(self, group_df):
        
        stats_df = self.stats_df
        mean_label = 'mean_activity_level_'
        stdev_label = 'stdev_activity_level_'
        #Extract Plate_and_Date and Control State to determine what plate to reference the Plate and either it's negative or positive control state statistics
        first_row_of_group = group_df.iloc[0]

        identifier = first_row_of_group['Plate_and_Date']

        #Reference values in statistics dataframe and save them
        reference_row = stats_df.loc[identifier]
        
        self.pos_control_info['mean'] = reference_row[mean_label + 'pos']
        self.pos_control_info['stdev'] = reference_row[stdev_label + 'pos']

        self.neg_control_info['mean'] = reference_row[mean_label + 'neg']
        self.neg_control_info['stdev'] = reference_row[stdev_label + 'neg']

    def calc_z_score(self, score, control_info):
        z_score = (score - control_info['mean']) / control_info['stdev']
        return z_score

#Function Declarations


def filter_to_needed_data(df):
    options = ['positive control (hit)','negative control']
    df = df[df["Control State"].isin(options)]
    return df[['Plate_and_Date','Control State', 'activity_level', 'Well']]

def operate(df_to_group, stats_df):

    # Subset to positive and negative control rows then subset to needed columns
    needed_data = filter_to_needed_data(df_to_group)

    #Group by "Plate_and_Date" and "Control State"
    grouped_data = needed_data.groupby(by=['Plate_and_Date'])

    z_score_controller = Calculate_Z_Score_Per_Control(stats_df)

    z_scores = grouped_data.apply(z_score_controller.main)

    z_scores.reset_index('Plate_and_Date', inplace=True)

    return z_scores

def main(data):

    for key in data:

        associated_data = data[key]

        prepped_data = associated_data[key_of_prepped_data]
        stats_per_plate = associated_data[key_of_stats_per_plate]

        processed_data = operate(prepped_data,stats_per_plate)

        associated_data['neg_and_pos_z_scored'] = processed_data

    return data