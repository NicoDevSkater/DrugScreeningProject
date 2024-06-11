import pandas as pd
import numpy as np
global key_of_summarized_data, key_of_prepped_data, key_of_meta_data
key_of_summarized_data = 'summary_table'
key_of_prepped_data = 'prepped_data'
key_of_meta_data ='meta_data'

def format_columns(df: pd.DataFrame, rename_obj) -> pd.DataFrame:

    return df.rename(rename_obj, axis='columns')

def change_column_dtype(df: pd.DataFrame, dtype_dict: dict) -> pd.DataFrame:

    df = df.astype(dtype_dict)
    
    return df

def operate(summary_df, prepped_df, meta_data):
    
    summary_rst_ndx = summary_df.reset_index()

    plate_date_split = prepped_df['Plate_and_Date'].str.split(expand=True)
    
    prepped_df['Plate'] = plate_date_split.loc[:,0]
    prepped_df['Run Date'] = plate_date_split.loc[:,1]

    rename_dict = meta_data['renamed_columns_mapped']
    rename_func = lambda col: col.replace(' ', '_')

    prepped_result = (
        prepped_df
        .pipe(pd.DataFrame.drop, columns = 'Plate_and_Date')
        .pipe(pd.DataFrame.rename, columns=rename_dict)
        .pipe(format_columns, rename_func)
        .pipe(change_column_dtype, {'Plate':'int64','Run_Date':'datetime64[ns]'})
    )

    summary_formatted =  format_columns(summary_rst_ndx, rename_func)
    
    prepped_df_only_compounds = prepped_result.query('Control_State == "compound"')
    summary_df_only_compounds = summary_formatted.query('Molecule_Name == Molecule_Name')

    beautify_func = lambda col: col.replace('_', ' ')
    merged = ( 
            pd.merge(summary_df_only_compounds, prepped_df_only_compounds,
                        on=['Molecule_Name', 'Structure_(CXSMILES)', 'Plate', 'Run_Date','Well'],
                        suffixes = ('_SUMMARY', '_CDD'),
                        )
            .rename(beautify_func, axis = 'columns')
            )
    
    return merged
    

def main(data):

    for key in data:

        associated_data = data[key]

        summary_data = associated_data[key_of_summarized_data]
        prepped_data = associated_data[key_of_prepped_data]
        meta_data = associated_data[key_of_meta_data]
        processed_data = operate(summary_data, prepped_data, meta_data)

        associated_data['compare_with_cdd_exports'] = processed_data

    return data
