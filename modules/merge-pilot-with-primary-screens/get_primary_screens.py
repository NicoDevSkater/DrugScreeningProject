#For now I'll just cherry pick Mpox, just to get the dat merged
import pandas as pd
import os 

primary_screens_path = os.getenv('PRIMARY_SCREENS')

primary_screen_file_names = os.listdir(primary_screens_path)

primary_file_names = [name for name in primary_screen_file_names if name == 'CDD CSV Export_Tuschl_Mpox_E1_E12_MTase_PrimaryScreen.csv']

def main(file_names = primary_file_names, path = primary_screens_path):

    for name in file_names:

        associated_data = pd.read_csv(path + name, low_memory=False)

        return associated_data, name


primary_dict = main()