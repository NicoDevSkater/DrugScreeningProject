from get_pilots import pilot_screens_dict
from get_primary_screens import primary_dict
# from merge_screens import main as merge_peas_and_peas

import pandas as pd
import os

primary_screens_path = os.getenv('PRIMARY_SCREENS')


def main():

    mpox_primary_df, file_name = primary_dict

    mpox_pilot_df = pilot_screens_dict['Mpox_E1_E12']

    merged = pd.concat([mpox_primary_df, mpox_pilot_df])

    merged.to_csv(primary_screens_path+ file_name, index = False)

main()