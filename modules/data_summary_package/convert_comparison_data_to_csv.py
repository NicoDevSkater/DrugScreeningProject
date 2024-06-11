import pandas as pd

global key_of_data_to_access
key_of_data_to_access = 'compare_with_cdd_exports'


def main(data):

    for key in data:

        associated_data = data[key]

        comparison_data = associated_data[key_of_data_to_access]
        # comparison_data.set_index('Molecule Name', inplace=True)
        path = '/Users/nbaez/Documents/DrugScreeningProject/drug_screening_NPI_per_compound/{}_stats.csv'.format(key)

        comparison_data.to_csv(path)

    return data