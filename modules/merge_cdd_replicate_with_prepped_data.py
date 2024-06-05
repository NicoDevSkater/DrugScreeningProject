import pandas as pd
import numpy as np
from prep_prepped_data_for_comparison import sars_cov2_prepped_needed
sars_cov2_to_compare = pd.read_csv('SARS_COV2_Compare_With_CDD_Export.csv')


# print(sars_cov2_to_compare)
# print(sars_cov2_prepped_needed)
dataframes = [sars_cov2_to_compare, sars_cov2_prepped_needed]


merged  = sars_cov2_to_compare.merge(sars_cov2_prepped_needed, left_on=['Molecule Name', 'Structure (CXSMILES)'], right_on=['Molecule Name', 'Structure (CXSMILES)'])
print(merged.columns)

merged.to_csv('SARS_COV2_Compare_Nico_With_Fraser.csv')