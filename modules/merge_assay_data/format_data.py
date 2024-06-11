import pandas as pd
import os
import sys
global npi_data_path
npi_data_path = os.getenv('MERGED_ASSAY_PATH')


def main(data):

    # format columns

    data.columns = [(col[0].replace('_',' '), col[1].replace('_',' ')) for col in data.columns]

    data.to_csv(npi_data_path + 'compound_stats_all_assays.csv')

    return data