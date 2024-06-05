import pandas as pd
import numpy as np
import math

com_uns_npi_info = pd.read_csv('SARS_COV2_Merged_Com_Uns_NPI_Info.csv')
uns_npi_info = pd.read_csv('SARS_COV2_NPI_Per_Unspecified_and_Error.csv')

#groupby plate
com_uns_npi_info_grouped = (com_uns_npi_info.groupby('Plate_and_Date'))
uns_npi_info_grouped = (uns_npi_info.groupby('Plate_and_Date'))

result_com_uns = com_uns_npi_info_grouped.agg({'NPI': ['mean','std','min','max']})
result_uns = uns_npi_info_grouped.agg({'NPI': ['mean','std'], 'NPI_Error': ['mean','std'],'Control State':'size'})

# Flatten the columns
result_com_uns.columns = ['_'.join(col).strip() for col in result_com_uns.columns.values]

#ADD difference of Max and Min column
max_NPIs = result_com_uns['NPI_max']
min_NPIs = result_com_uns['NPI_min']

result_com_uns['Max - Min'] = max_NPIs - min_NPIs  

result_com_uns.to_csv('SARS_COV2_com_uns_npi_stats.csv')
# result_uns.to_csv('SARS_COV2_uns_npi_stats.csv')
