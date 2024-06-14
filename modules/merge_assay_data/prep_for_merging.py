import pandas as pd
import os
import sys
modulse_path = os.getenv('MODULES_PATH')

sys.path.append(modulse_path)

from utils.utilities import get_needed_path, strip_after_substring

with_prepped_path = get_needed_path(__file__ , '/DrugScreeningProject', '/drug_screening_data_merged_with_prepped/')

#Get list of files in target directory
files = os.listdir(with_prepped_path)
#filter to files that are comma seperated
csv_file_names = [file for file in files if file.endswith('.csv')]

def drop_uneeded_columns(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:

    return df.drop(columns=columns_to_drop)

def format_columns(df: pd.DataFrame, rename_obj) -> pd.DataFrame:

    return df.rename(rename_obj, axis='columns')

def combine_columns(df: pd.DataFrame, column_1: str, column_2: str) -> pd.DataFrame:

    df[column_1 + "_and_" + column_2] = df[column_1].astype(str) +'_'+ df[column_2].astype(str)

    return df

def main(file_names = csv_file_names , path = with_prepped_path) :

    data_dict = {}

    for file_name in file_names: 

        associated_data = pd.read_csv(path + file_name, low_memory=False, index_col = [0])

        rename_func = lambda col: col.replace(' ', '_')

        data_formatted = format_columns(associated_data, rename_func)

        remove_heading = 'Tuschl_'

        key = strip_after_substring(file_name.replace(remove_heading, ''),'_PrimaryScreen')

        data_dict[key] = data_formatted

    return data_dict
