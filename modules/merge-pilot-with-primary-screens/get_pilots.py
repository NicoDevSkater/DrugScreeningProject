import os
import pandas as pd
pilot_screens_path = os.getenv('PILOT_SCREENS')

pilot_screens_dir_file_names = os.listdir(pilot_screens_path)

pilot_file_names = [name for name in pilot_screens_dir_file_names if name.endswith('csv')]



def main(file_names = pilot_file_names, path = pilot_screens_path):

    data_dict = {}

    for name in file_names:

        associated_data = pd.read_csv(path + name)
        remove_leading = "CDD CSV Export_Tuschl_"
        remove_after = "_Pilot_"

        leading_removed = name.replace(remove_leading ,'')

        protein, after_substring = leading_removed.split(remove_after)

        day_sequence = after_substring.split('.')[0]

        if not protein in data_dict:

            data_dict[protein] = {}

        data_dict[protein][day_sequence] = associated_data

    return data_dict

pilot_screens_dict = main()


