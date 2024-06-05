import pandas as pd
import os 

import sys
sys.path.append('/Users/nbaez/Documents/DrugScreeningProject/drugScreeningProcessing/modules')

from utils.utilities import strip_path

raw_data_path = strip_path(os.path.abspath(__file__), 4) + '/drug_screening_raw_data/'

#Get list of files in target directory
files = os.listdir(raw_data_path)
#filter to files that are comma seperated
csv_file_names = [file for file in files if file.endswith('.csv')]

def main(raw_data_file_names, path):

    data_dict = {}

    for file_name in raw_data_file_names: 

        associated_data = pd.read_csv(path + file_name, low_memory=False)
        
        remove_heading = 'CDD CSV Export_'
        remove_ending = '.csv' 

        key = file_name.replace(remove_heading, '').replace(remove_ending, '')

        data_dict[key] = {'prepped_data':associated_data,
                          'meta_data':{}}

    return data_dict

screening_data_mapped = main(csv_file_names, raw_data_path)