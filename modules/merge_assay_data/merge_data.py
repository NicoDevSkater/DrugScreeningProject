import pandas as pd


def operate(data_dict: dict[str, pd.DataFrame]):

    merged = pd.concat(data_dict, axis= 1)

    # MERGE ASSAY DATA ON BY PLATE AND WELL
    # Extract the Plate_and_Well columns for each group

    plate_and_well_columns = [col for col in merged.columns if 'Plate_and_Well' in col]

    plate_and_well_combined = pd.concat([merged[col] for col in plate_and_well_columns])

    plate_and_well_na_dropped = plate_and_well_combined.dropna()

    plate_and_well_na_dropped.name = 'Plate_and_Well'

    # Set the long series as the index of the original DataFrame
    merged_reindexed = merged.reindex(plate_and_well_na_dropped.index)
    
    set_index_to_plate_well = merged_reindexed.set_index(plate_and_well_na_dropped)

    # Drop the Plate_and_Well columns from the DataFrame
    plate_well_columns_dropped = set_index_to_plate_well.drop(plate_and_well_columns, axis=1)

    # plate_well_columns_dropped.head().to_csv('merging_testing.csv', index=False)
    return plate_well_columns_dropped


def main(data):

    processed_data = operate(data)

    return processed_data