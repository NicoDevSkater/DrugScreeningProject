from .get_z_score_per_neg_pos_controls import main as neg_pos_zscores
from .determine_outliers import main as find_outliers
from .kill_outliers_in_prepped import main as kill_outliers

def main(data):

    neg_pos_zscores_calculated = neg_pos_zscores(data)

    outliers_found = find_outliers(neg_pos_zscores_calculated)

    outliers_killed = kill_outliers(outliers_found)

    return outliers_killed