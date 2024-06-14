import pandas as pd


global key_of_data_to_access
key_of_data_to_access = 'prepped_data'

def operate(df):
     
    grouped = df.groupby(['Plate_and_Date', 'Control State'])

    stats_calculated = grouped.agg({'activity_level' : ['sum','mean','std','size']})

    stats_pvt_tbl = pd.pivot_table(stats_calculated, index='Plate_and_Date', columns = 'Control State')

    stats_pvt_tbl.columns = [format_columns(col) for col in stats_pvt_tbl.columns]

    stats_pvt_tbl['total_wells'] = stats_pvt_tbl["total_pos"] + stats_pvt_tbl["total_neg"] + stats_pvt_tbl["total_com"] + stats_pvt_tbl["total_uns"]

    return stats_pvt_tbl
def format_columns(column : tuple[str,str,str]) -> str:

    activity_level , agg_method, control_state = column

    suffix = control_state[:3]

    if agg_method == 'size':

        return "_".join(['total',suffix])
    
    elif agg_method == 'std':

        agg_method = 'stdev'

    return '_'.join([agg_method , activity_level, suffix])

def main(data):
    
    for key in data:
        
        associated_data = data[key]

        dataframe = associated_data[key_of_data_to_access]

        processed_data =  operate(dataframe)

        associated_data['control_state_stats'] = processed_data

    return data