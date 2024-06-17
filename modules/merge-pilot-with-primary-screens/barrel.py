from get_pilots import pilot_screens_dict
from get_primary_screens import primary_screens_dict
from merge_screens import main as merge_peas_and_peas

import pandas as pd
import os

primary_screens_path = os.getenv('PRIMARY_SCREENS')


def main():

    merge_peas_and_peas(pilot_screens_dict, primary_screens_dict)

    

main()