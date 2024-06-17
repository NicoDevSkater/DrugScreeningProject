#For now I'll just cherry pick Mpox, just to get the dat merged
import pandas as pd
import os 

primary_screens_path = os.getenv('PRIMARY_SCREENS')

primary_screen_file_names = os.listdir(primary_screens_path)

primary_file_names = [name for name in primary_screen_file_names if name.endswith('.csv')]

def main(file_names = primary_file_names, path = primary_screens_path):

    data_dict = {}

    for name in file_names:

        associated_data = pd.read_csv(path + name)
        remove_leading = "CDD CSV Export_Tuschl_"
        remove_ending : str = None

        if 'NTase' in name:

            remove_ending = "_NTase"
            
        elif 'MTase' in name:

            remove_ending = "_MTase"

        protein = name.replace(remove_leading ,'').split(remove_ending)[0]

        data_dict[protein] = associated_data

    return data_dict


primary_screens_dict = main()