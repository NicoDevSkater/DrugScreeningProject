import pandas as pd


global key_of_zscores, key_of_stats_per_plate
key_of_zscores = 'neg_and_pos_z_scored'
key_of_stats_per_plate = 'stats_per_plate'
#Questions before I proceed

#How will I know if a lum reading of an outlier is too high or too low?
    #I think I will know by looking at the z score of data points that hit the parameters
    #if the z_score is negative then the outlier is too low, if it is positive then it is too high

#What do  Multiple Outlier parameters vs Single Parameters represent?
#When should I employ Multi outlier versus single outlier parameters?

#Do use max_CV or each row's own cv value

#Create a parameters class, each instace will equip itself with the necessary parameter values to use to find outliers
class Outlier_Parameters:

    def __init__(self, screen_type):

        if screen_type == 'mtase':
            #neg single, too low
            self.neg_single_low_zscore = -3.4
            self.neg_single_low_cv = 0.15
            
            #neg multi, too low
            self.neg_multi_low_zscore = -2.5 
            self.neg_multi_low_cv = 0.3

            #for multi outlier checks first check if the z score is in between -2.5 and -3.4 THEN check if the cv is greater than or equal tp 0.3


            #neg single, too high
            self.neg_single_high_zscore = 3.3
            self.neg_single_high_cv = 0.04

            #pos single, too high
            self.pos_single_high_zscore = 3.4
            self.pos_single_high_cv = 0.3

            #pos single, too low
            self.pos_single_low_zscore = -3.4
            self.pos_single_low_cv = 0.15

    def postive_multi(self):

        pass

    def is_pos_control_outlier(self, data_point_zscore, data_point_cv):

        outlier_type = 'non_outlier'

        if (data_point_zscore <= self.pos_single_low_zscore) and (data_point_cv >= self.pos_single_low_cv):

            outlier_type = 'single, too low'
        
        elif (data_point_zscore >= self.pos_single_high_zscore) and (data_point_cv >= self.pos_single_high_cv):

            outlier_type = 'single, too high'

        return outlier_type

    
    def is_neg_control_outlier(self, data_point_zscore, data_point_cv):

        outlier_type = 'non_outlier'

        if ((data_point_zscore <= self.neg_multi_low_zscore) and (data_point_zscore >= self.neg_single_low_zscore) ) and (data_point_cv >= self.neg_multi_low_cv):

            outlier_type = 'multi, too low'
        
        elif (data_point_zscore <= self.neg_single_low_zscore) and (data_point_cv >= self.neg_single_low_cv):

            outlier_type = 'single, too low'
        
        elif (data_point_zscore >= self.neg_single_high_zscore) and (data_point_cv >= self.neg_single_high_cv) :

            outlier_type = 'single, too high'

        return outlier_type


def describe_group_data_points(group_data, group_cv, outlier_controller):

    df_to_operate = group_data.copy()

    cntrl_state_column = df_to_operate['Control State']

    #Add empty column "is_outlier"

    neg_cntrl_rows = df_to_operate[cntrl_state_column == 'negative control'].copy()
    pos_cntrl_rows = df_to_operate[cntrl_state_column == 'positive control (hit)'].copy()

    neg_cntrl_rows['is_outlier'] = neg_cntrl_rows['z_score'].apply(outlier_controller.is_neg_control_outlier, args = (group_cv,))
    pos_cntrl_rows['is_outlier'] = pos_cntrl_rows['z_score'].apply(outlier_controller.is_pos_control_outlier, args = (group_cv,))

    cntrl_states_joined = pd.concat([neg_cntrl_rows,pos_cntrl_rows])
    
    return cntrl_states_joined

def operate(zscores_df, stats_df):

    to_return = pd.DataFrame(columns=['Plate_and_Date', 'Control State', 'activity_level', 'Well', 'z_score', 'is_outlier'])
    #first create an instance of Outlier_Parameters to set parameters
    #pass in the screen type as a parameter

    params = Outlier_Parameters('mtase') 

    for _, row in stats_df.iterrows():

        row_id = row.name
        
        associated_max_cv = row['max_Coefficient_Variation']
        associated_data = zscores_df[zscores_df['Plate_and_Date'] == row_id]

        to_return = pd.concat([to_return,describe_group_data_points(associated_data, associated_max_cv, params)])

    return to_return

def main(data):

    for key in data:

        associated_data = data[key]

        z_scores = associated_data[key_of_zscores]
        stats_per_plate = associated_data[key_of_stats_per_plate]
        
        processed_data = operate(z_scores, stats_per_plate)
        
        associated_data['control_points_outlier_status'] = processed_data

        del associated_data[key_of_zscores]

    return data
