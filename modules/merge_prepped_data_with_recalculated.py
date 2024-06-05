import pandas as pd
import numpy as np
import math
from scipy.stats import norm

#Import CSV files
sars_cov2_stats_no_outliers = pd.read_csv("SARS_COV2_Recalculated_Without_Outliers.csv")
sars_cov2_raw_prepped = pd.read_csv("prepped_sars_cov2_screening.csv")

#subset dataframes to needed columns
def subset_to_needed_columns(df,columns):
    return df[columns]

columns_to_subset_prepped = ['Plate_and_Date','Molecule Name','Structure (CXSMILES)','Batch Name','Well','Control State','LUM (RLU)']
columns_to_subset_stats_recalced = ['Plate_and_Date','Control State','mean','std','Z_prime','Well']

sars_cov2_prepped_columns_subsetted = subset_to_needed_columns(sars_cov2_raw_prepped,columns_to_subset_prepped)
sars_cov2_recalced_columns_subsetted = subset_to_needed_columns(sars_cov2_stats_no_outliers, columns_to_subset_stats_recalced)

def merge_dfs(df1, df2):
    return df1.merge(df2,how='outer')

sars_cov2_merged = merge_dfs(sars_cov2_prepped_columns_subsetted, sars_cov2_recalced_columns_subsetted)

#Set index to "Plate_and_Date" to all dataframes
def set_index_to_id(df):
    df.set_index("Plate_and_Date", inplace=True)

set_index_to_id(sars_cov2_merged)

print(sars_cov2_merged)
sars_cov2_merged.to_csv('SARS_COV2_Merged_Recalculations_And_Prepped.csv')
# sars_cov2_merged.to_csv('SARS_COV2_Merged_Recalculations_And_Preppedtest.csv')

