from .merge_needed_data import main as merge_data
from .beautify_data import main as format_data
from .merge_summary_data_with_prepped_data import main as merge_summary_with_prepped
from .convert_comparison_data_to_csv import main as convert_data_to_csv

def main(data):
    
    return convert_data_to_csv(merge_summary_with_prepped(format_data(merge_data(data))))