import pandas as pd

mpox_data = pd.read_csv('drug_screening_NPI_per_compound/Tuschl_Mpox_E1_E12_MTase_PrimaryScreen_stats.csv', index_col = 0)
zika_data = pd.read_csv('drug_screening_NPI_per_compound/Tuschl_ZIKA_NS5_MTase_PrimaryScreen_stats.csv', index_col=0)

def combine_columns(df: pd.DataFrame, column_1: str, column_2: str) -> pd.DataFrame:

    df[column_1 + "_and_" + column_2] = df[column_1].astype(str) +'_'+ df[column_2].astype(str)

    return df

mpox_combined = combine_columns(mpox_data, 'Plate','Well')
zika_combined = combine_columns(zika_data, 'Plate','Well')

mpox_combined.set_index('Plate_and_Well', inplace=True)
zika_combined.set_index('Plate_and_Well', inplace=True)

merged = pd.concat([zika_combined,mpox_combined], axis=1, join='outer')

# merged_changed = merged_data.set_index('Plate_and_Well')

x = 6