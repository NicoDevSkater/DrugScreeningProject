import pandas as pd

global key_of_summarized_data
key_of_summarized_data = 'summary_table'




def operate(summary_df):

    summary_df.reset_index(inplace=True)
    summary_df.set_index('Molecule Name',inplace=True)

    plate_date_column = summary_df['Plate_and_Date']

    summary_df['Plate'] = plate_date_column.apply(lambda str:int(str.split(' ')[0]))
    summary_df['Run Date'] = plate_date_column.apply(lambda str:pd.to_datetime(str.split(' ')[1]))

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

    summary_df.rename(columns=rename_dict, inplace=True)

    sorting_dict = [
        'Structure (CXSMILES)','Batch Name','Run Date','Plate','Well','NPI','Delta NPI','Z Score NPI',
        'Average NPI','Stdev NPI','Max NPI','Min NPI','Max NPI - Min NPI','Z Prime','Has Outliers','Z Prime Pre Correction'
    ]    

    summary_df_sorted = summary_df[sorting_dict]

    return summary_df_sorted




def main(data):

    for key in data:

        associated_data = data[key]

        summary_data = associated_data[key_of_summarized_data]

        processed_data = operate(summary_data)

        associated_data[key_of_summarized_data] = processed_data

    return data

