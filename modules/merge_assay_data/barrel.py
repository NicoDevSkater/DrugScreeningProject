from .prep_for_merging import main as prep_assay_data
from .merge_data import main as merge_assay_data
from .format_data import main as format_assay_data

def main():

    formatted = prep_assay_data()

    merged = merge_assay_data(formatted)

    return format_assay_data(merged)
