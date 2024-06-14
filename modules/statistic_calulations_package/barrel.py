from .get_ZPrime_per_plate import main as z_primes
from .get_coefficient_of_variation import main as CVs
from .calculate_simple_stats import main as simple_stats

def main(data):

    return CVs(z_primes(simple_stats(data)))