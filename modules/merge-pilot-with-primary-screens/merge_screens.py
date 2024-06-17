import pandas as pd
import os

raw_data_path = os.getenv('RAW_DATA')

def main (pilots_dict, primaries_dict):

    data_dict = {}

    dict_for_iter = None
    other_dict = None

    if len(pilots_dict.keys()) > len(primaries_dict.keys()) :

        dict_for_iter = pilots_dict
        other_dict = primaries_dict

    else: 
        dict_for_iter = primaries_dict 
        other_dict = pilots_dict

    for key in dict_for_iter:

        if not key in other_dict:

            dict_for_iter[key].to_csv(raw_data_path + key + '.csv', index = False)

            continue

        associated_data = dict_for_iter[key]

        other_associated_data = other_dict[key]

        together = [associated_data, *other_associated_data.values()]

        merged = pd.concat(together)

        merged.to_csv(raw_data_path + key + '.csv', index = False)