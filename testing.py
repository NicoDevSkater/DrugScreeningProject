import pandas as pd
import os


npi_per_compound_path = os.getenv('NPI_DATA_PATH')
all_data_path = os.getenv('MERGED_ASSAY_PATH')


npi_file_names = os.listdir(npi_per_compound_path)[1:]
all_data_file_name = os.listdir(all_data_path)[1:][0]

# def main1(files_names, path):

#     dataframes = list(map(lambda x: pd.read_csv(path+x, index_col=0), files_names))

#     molecule_name_cols = list(map(lambda y: y['Molecule Name'], dataframes))

#     all_together = pd.concat(molecule_name_cols)



#     f =7

# main1(npi_file_names, npi_per_compound_path)

def main2(file_name, path):

    #Read merged data of all 7 assays into memory
    dataframe = pd.read_parquet(path+file_name)

    #Extract all molecule name (RU identifier) columns from each assay
    cols_to_process = [col for col in dataframe.columns if col.split(';')[1] == 'Molecule Name']
    to_series = list(map(lambda col: dataframe[col],cols_to_process))

    #Concatenate all molecule name columns from all 7 assays together
    all_together = pd.concat(to_series)

    #Convert list into a set
    #Converting a list into a set removes all duplicate value Ex.[1,2,3,3,3,4] -> [1,2,3,4]
    duplicates_removed = set(all_together)

    #Print the length of the set
    print('unique compounds, all assays',len(duplicates_removed))


main2(all_data_file_name, all_data_path)