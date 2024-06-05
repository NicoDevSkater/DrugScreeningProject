import pandas as pd
import math

global key_of_prepped_data, key_of_stats_per_plate
key_of_prepped_data = 'prepped_data'
key_of_stats_per_plate = 'stats_per_plate'


class NPI_Controller:

    def __init__(self, prepped_data, stats_per_plate):

        self.prepped_data = prepped_data
        self.stats_per_plate = stats_per_plate
        self.npi_data = pd.DataFrame(prepped_data).set_index('Plate_and_Date')


    def calculate_npi(self,datapoint_score, negative_mean, positive_mean) -> float:
       
        a = negative_mean - datapoint_score
        b = negative_mean - positive_mean
        c = a / b
        npi = c * 100
 
        return npi
    
    def calculate_delta_npi(self, df, neg_mean, pos_mean, neg_std, pos_std) -> float:

        measurement = df['activity_level']
        npi = df['NPI']

        a = neg_mean - measurement
        b = neg_mean - pos_mean
        a_std = neg_std
        b_std = math.sqrt(( a_std ** 2 ) + ( pos_std ** 2 ))

        delta_npi = npi * math.sqrt( (( a_std / a ) ** 2 ) + (( b_std / b ) ** 2 ) )
        return delta_npi
    
    def calculate_zscore_npi(self, df):

        zscore_npi = (df['NPI'] - df['avg_NPI']) / df['stdev_NPI']
        return zscore_npi
    
    def main(self):

        for plate_stats in self.stats_per_plate.iterrows():

            id = plate_stats[0]
            
            values = plate_stats[1]

            plate_neg_mean = values['mean_activity_level_neg']
            plate_pos_mean = values['mean_activity_level_pos']
            plate_neg_stdev = values['stdev_activity_level_neg']
            plate_pos_stdev = values['stdev_activity_level_pos']

            self.npi_data.loc[id,'NPI'] = self.npi_data.loc[id,'activity_level'].apply(self.calculate_npi, args = (plate_neg_mean, plate_pos_mean))
            self.npi_data.loc[id,'delta_NPI'] = self.npi_data.loc[id].apply(self.calculate_delta_npi, axis = 1, args = (plate_neg_mean, plate_pos_mean, plate_neg_stdev, plate_pos_stdev))
            
            npi_stats = self.npi_data.loc[id,'NPI'].agg(['mean','std','min','max'])
        
            self.npi_data.loc[id,'avg_NPI'] = npi_stats['mean']
            self.npi_data.loc[id,'stdev_NPI'] = npi_stats['std']
            self.npi_data.loc[id,'min_NPI'] = npi_stats['min']
            self.npi_data.loc[id,'max_NPI'] = npi_stats['max']
            
            self.npi_data.loc[id,'max_NPI - min_NPI'] = self.npi_data.loc[id, 'max_NPI'] - self.npi_data.loc[id, 'min_NPI']
            self.npi_data.loc[id,'z_score_NPI'] = self.npi_data.loc[id].apply(self.calculate_zscore_npi, axis=1)
        
        return self.npi_data


def subset_to_needed_data(df, rows = None, columns = None):

    if rows is None and columns is None:
        return df
    elif rows is None:
        return df[columns]
    elif columns is None:
        return df.loc[rows]
    else:
        return df.loc[rows, columns]


def operate(prepped_data_df, stats_df):

    prepped_needed_columns = ['Plate_and_Date', 'Well', 'activity_level', 'Molecule Name', 'Structure (CXSMILES)', 'Batch Name', 'Control State' ]
    prepped_needed_rows_boolean = prepped_data_df['Control State'].isin(['compound', 'unspecified control'])

    stats_needed_columns = ['mean_activity_level_neg', 'mean_activity_level_pos', 'stdev_activity_level_neg', 'stdev_activity_level_pos']
    
    needed_prepped = subset_to_needed_data(prepped_data_df, rows = prepped_needed_rows_boolean, columns = prepped_needed_columns)
    needed_stats = subset_to_needed_data(stats_df, columns = stats_needed_columns)

    npi_controller = NPI_Controller(needed_prepped, needed_stats)
    npi_data = npi_controller.main()

    return npi_data




def main(data):

    for key in data:

        associated_data = data[key]

        prepped_data = associated_data[key_of_prepped_data]

        stats_per_plate = associated_data[key_of_stats_per_plate]

        processed_data = operate(prepped_data, stats_per_plate)

        associated_data['npi_stats'] = processed_data
    
    return data