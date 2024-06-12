import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import fastparquet
import os


global npi_data_path
npi_data_path = os.getenv('MERGED_ASSAY_PATH')


def main(data):

    # format columns

    data.columns = pd.MultiIndex.from_tuples([(col[0].replace('_',' '), col[1].replace('_',' ')) for col in data.columns])

    data.columns = [';'.join(col) for col in data.columns]

    data.to_parquet(npi_data_path + 'compound_stats_all_assays.parquet')

    return data