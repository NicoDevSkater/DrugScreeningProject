from raw_to_prepped.prep_input_data import prepped_data
from statistic_calulations_package.barrel import main as calculate_statistics
from recalculation_prep.barrel import main as prep_for_recaulculation
from npi_and_npi_stats_package.barrel import main as calculate_npi_and_npi_stats
from data_summary_package.barrel import main as summarize_data
# Now you can use the prepped_data variable



before_recalculations = calculate_statistics(prepped_data)

prepped_for_recalculation = prep_for_recaulculation(before_recalculations)

data_recalculated = calculate_statistics(prepped_for_recalculation)

npi_data = calculate_npi_and_npi_stats(data_recalculated)

summary_data = summarize_data(npi_data)  