from .get_control_counts import main as counts
from .get_control_lum_sum import main as sums
from .merge_counts_and_sums import main as merged
from .get_control_lum_mean import main as means
from .get_control_lum_stdev import main as stdevs
from .get_ZPrime_per_plate import main as z_primes
from .get_coefficient_of_variation import main as CVs

def main(data):

    return CVs(z_primes(stdevs(means(merged(sums(counts(data)))))))