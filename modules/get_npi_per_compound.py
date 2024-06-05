import pandas as pd
import numpy as np
import math


#Import CSV files
sars_cov2_recalculations_prepped_merged = pd.read_csv("SARS_COV2_Merged_Recalculations_And_Prepped.csv")

#Since we are calculating npi and npi error per compound we don't need rows with unspecides controls

sars_cov2_recalculations_prepped_merged_subsetted = sars_cov2_recalculations_prepped_merged[sars_cov2_recalculations_prepped_merged['Control State'] != 'unspecified control']
print(sars_cov2_recalculations_prepped_merged_subsetted)
#group by plate_and_date
def group_by_plate_date(df):
    return df.groupby('Plate_and_Date')

sars_cov2_grouped = group_by_plate_date(sars_cov2_recalculations_prepped_merged_subsetted)

def calculate_npi_error_propagation(compound_measurement, compound_npi, neg_mean, pos_mean, neg_std, pos_std):
    a = neg_mean - compound_measurement
    b = neg_mean - pos_mean
    a_std = neg_std
    b_std = math.sqrt(( a_std ** 2 ) + ( pos_std ** 2 ))

    delta_npi = compound_npi * math.sqrt( (( a_std / a) ** 2 ) + (( b_std / b) ** 2 ) )
    return delta_npi



def iterate_and_operate(df_to_iterate, neg_mean, pos_mean, neg_std, pos_std):

    for index, row in df_to_iterate.iterrows():
        
        #get current row's measured score
        compound_measurement = row['LUM (RLU)']
        #calculate npi
        compound_npi = calculate_npi(compound_measurement, neg_mean, pos_mean)
        #calculate delta npi: error propagation
        compound_npi_error = calculate_npi_error_propagation(compound_measurement, compound_npi, neg_mean, pos_mean, neg_std, pos_std)
        #save npi to row
        df_to_iterate.loc[index,'NPI'] = compound_npi
        df_to_iterate.loc[index,'NPI_Error'] = compound_npi_error
        
    
    return df_to_iterate

def set_column_to_index(df, column_name):
    df.set_index(column_name, inplace=True)

def remove_certain_columns(df, columns_to_drop):
    df.drop(columns=columns_to_drop, inplace=True)

def main(df): 
    
    #create three subsets 1: compound measuremnts 2: negative control measurements 3: positive control measurements
    compound_measurements = df[df['Molecule Name'].notna()]
    neg_control_measurments = df[df['Control State'] == 'negative control']
    pos_control_measurements = df[df['Control State'] == 'positive control (hit)']

    #get means of positive and negative control states
    neg_mean_score = neg_control_measurments['mean'].to_numpy()[0]
    pos_mean_score = pos_control_measurements['mean'].to_numpy()[0]
    neg_std_score = neg_control_measurments['std'].to_numpy()[0]
    pos_std_score = pos_control_measurements['std'].to_numpy()[0]
    

    compound_npis_calculated = iterate_and_operate(compound_measurements, neg_mean_score, pos_mean_score, neg_std_score, pos_std_score)



    # print(compound_npis_calculated)

    #get z_prime value of plate from either positive or negative control data frames
    plate_z_prime = neg_control_measurments['Z_prime'].to_numpy()[0]
    #add z_prime of plate to compound measurments data frame
    compound_npis_calculated['Z_prime'] = plate_z_prime
    compound_npis_calculated['neg_mean_score'] = neg_mean_score
    compound_npis_calculated['pos_mean_score'] = pos_mean_score
    compound_npis_calculated['neg_std'] = neg_std_score
    compound_npis_calculated['pos_std'] = pos_std_score

    compound_npis_calculated.drop(columns=['Plate_and_Date','mean', 'std'], inplace=True)
    return compound_npis_calculated
    



sars_cov2_npis_calculated = sars_cov2_grouped.apply(main)
sars_cov2_npis_calculated.reset_index(inplace=True)


column_to_drop = 'level_1'
remove_certain_columns(sars_cov2_npis_calculated, column_to_drop)

column_to_index_by = 'Molecule Name'
set_column_to_index(sars_cov2_npis_calculated, column_to_index_by)

sars_cov2_npis_calculated.to_csv('SARS_COV2_NPI_Per_Compound_and_Error.csv')
