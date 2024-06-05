from generate_cdd_export_replicate_table import merged2
import pandas as pd

"""
I need to change the fomratting of the cdd_export_replicate datasets

First I need to make the "Molecule Name" column the index
Then I need to seperate the "Plate_and_Date" columns in to there original columns "Plate" int datatype and "Date" date datatype
After that I need to rename most columns
"""

merged2.reset_index(inplace=True)
merged2.set_index('Molecule Name',inplace=True)

plate_date_column = merged2['Plate_and_Date']

merged2['Plate'] = plate_date_column.apply(lambda str:int(str.split(' ')[0]))
merged2['Run Date'] = plate_date_column.apply(lambda str:pd.to_datetime(str.split(' ')[1]))

merged2.drop(columns='Plate_and_Date',inplace=True)

rename_dict = {
    'delta_NPI':'Delta NPI',
    'z_score_NPI':'Z Score NPI',
    'avg_NPI':'Average NPI',
    'stdev_NPI':'Stdev NPI',
    'min_NPI':'Min NPI',
    'max_NPI':'Max NPI',
    'max_NPI - min_NPI':'Max NPI - Min NPI',
    'Z_prime':'Z Prime',
    'has_outliers':'Has Outliers',
    'prev_Z_prime':'Z Prime Pre Correction',
}
merged2.rename(columns=rename_dict, inplace=True)

columns_orderd = [
    'Structure (CXSMILES)','Batch Name','Run Date','Plate','Well','NPI','Delta NPI','Z Score NPI',
    'Average NPI','Stdev NPI','Max NPI','Min NPI','Max NPI - Min NPI','Z Prime','Has Outliers','Z Prime Pre Correction'
]
merged2_sorted = merged2[columns_orderd]

#filter rows that have Stucture signatures
merged2_filtered = merged2_sorted[merged2_sorted['Structure (CXSMILES)'].notna()]

merged2_filtered.to_csv('SARS_COV2_Compare_With_CDD_Export.csv')