import pandas as pd
import os 



global key_of_data_to_access
key_of_data_to_access = 'compare_with_cdd_exports'


def main(data, dir_to_upload_at = os.getenv("MERGED_WITH_PREPPED")):

    for key in data:

        associated_data = data[key]

        comparison_data = associated_data[key_of_data_to_access]
        # comparison_data.set_index('Molecule Name', inplace=True)
        path = dir_to_upload_at + '{}_stats.csv'.format(key)

        comparison_data.to_csv(path)

    return data