import pandas as pd
import numpy as np

#Import csv
sars_cov2_prepped_data = pd.read_csv('drug_screening_prepped/NSP14 SARS COV2 Tuschl Lab Primary Screen.csv')

sars_cov2_compound_only = sars_cov2_prepped_data[sars_cov2_prepped_data['Control State'] == 'compound control']

needed_columns = [
    'Molecule Name', 'Structure (CXSMILES)','Batch Name','Run Date','Plate','Well','LUM (RLU)',"LUM (RLU) Z'-factor",'NPI @ 25 µM (%)','LUM z score'
]
sars_cov2_prepped_needed = sars_cov2_compound_only[needed_columns]

