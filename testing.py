import pandas as pd
import os


npi_per_compound_path = os.getenv('MERGED_WITH_PREPPED')
all_data_path = os.getenv('MERGED_ASSAY_PATH')


mmu_cgas = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_Mmu_cGAS_NTase_PrimaryScreen_stats.csv', index_col = 0)
mpox = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_Mpox_E1_E12_MTase_PrimaryScreen_stats.csv', index_col = 0)
# zika = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_ZIKA_NS5_MTase_PrimaryScreen_stats.csv', index_col = 0)
# sars = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_SARS_NSP14_MTase_PrimaryScreen_stats.csv', index_col = 0)
# ram = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_hum_RNMT_RAM_MTase_PrimaryScreen_stats.csv', index_col = 0)
# mettl = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_hum_METTL3_14_MTase_PrimaryScreen_stats.csv', index_col = 0)
# hsa_cgas = pd.read_csv('drug_screening_data_merged_with_prepped/Tuschl_Hsa_cGAS_NTase_PrimaryScreen_combined_stats.csv', index_col = 0)

print('mmu cgas length', len(mmu_cgas))
print('mpox length', len(mpox))
# print('zika length', len(zika))
# print('sars length', len(sars))
# print('ram length', len(ram))
# print('mettl lenth', len(mettl))
# print('hsa_cgas length', len(hsa_cgas))

dict = {
    'hum_cgas':mmu_cgas,
    'mpox':mpox,
#     'zika': zika,
#     'sars': sars,
#     'ram': ram,
#     'hsa_cgas': hsa_cgas,
#     'mettl' : mettl
}

merged = pd.concat(dict, axis = 1, ignore_index = False)