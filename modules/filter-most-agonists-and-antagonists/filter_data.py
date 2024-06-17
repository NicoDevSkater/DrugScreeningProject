import pandas as pd
import numpy as np
import os
import sys 
all_assay_data_dir_path = os.getenv('MERGED_ASSAY_PATH')

# all_assay_data_file_path = os.listdir(all_assay_data_dir_path)[1]


class Apply_Parameters :

    def __init__(self, dataframe):
    
        self.data = dataframe

        self.assay_labels = list({t[0] for t in dataframe.columns}) 

    def is_valid_npi(self,row_npi):

        return row_npi >= 20 or row_npi <= -20
    
    def is_valid_z_score_npi(self,row_z_score_npi):
        
        return row_z_score_npi >= 2 or row_z_score_npi <= -2

        
    def main(self, row):


        for assay_label in self.assay_labels:

            compound_npi_in_assay = float(row[(assay_label, 'NPI')])
            compound_z_score_npi_in_assay = float(row[(assay_label, 'Z Score NPI')])

            if pd.isna(compound_npi_in_assay):

                continue

            if self.is_valid_npi(compound_npi_in_assay) and self.is_valid_z_score_npi(compound_z_score_npi_in_assay):

                return True

        return False
        




def main(data_dir_path, data_file_path = 'mpox-mmu_cgas-merged.csv'):

    # data_read = pd.read_parquet(data_dir_path + data_file_path)

    data_read = pd.read_csv(data_dir_path + data_file_path, low_memory=False)

    # data_read.columns = pd.MultiIndex.from_tuples([tuple(col.split(';')) for col in data_read.columns])

    first_row = data_read.iloc[0]

    #Create a multi-index from the column names and the first row
    multi_index = pd.MultiIndex.from_tuples([(col.split('.')[0], first_row[col]) for col in data_read.columns])

    #Assign the new multi-index to the columns of the DataFrame
    data_read.columns = multi_index

    # Step 5: Drop the first row as it is now part of the multi-index
    data_read = data_read.drop(data_read.index[0])

    parameters = Apply_Parameters(data_read)

    data_subset = data_read[data_read.apply(parameters.main, axis=1)]

    dir_to_save_at = os.getenv('NOISE_FILTERED_PATH')

    data_subset.to_csv(dir_to_save_at + 'all_assay_data_noise_filtered.csv', index = False)

main(all_assay_data_dir_path)