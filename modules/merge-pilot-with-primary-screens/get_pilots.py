import os
import pandas as pd
pilot_screens_path = os.getenv('PILOT_SCREENS')

pilot_screens_dir_file_names = os.listdir(pilot_screens_path)

pilot_file_names = [name for name in pilot_screens_dir_file_names if name.endswith('csv')]



def main(file_names = pilot_file_names, path = pilot_screens_path):

    data_dict = {}

    for name in file_names:

        associated_data = pd.read_csv(path + name)
        remove_leading = "CDD_CSV_Export_Tuschl_"
        remove_after = "_Pilot"

        leading_removed = name.replace(remove_leading ,'')

        key = leading_removed.split(remove_after)[0]

        data_dict[key] = associated_data

    return data_dict

pilot_screens_dict = main()


