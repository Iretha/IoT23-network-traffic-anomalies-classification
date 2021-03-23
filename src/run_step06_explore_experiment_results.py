import logging
import warnings
import numpy as np
import sklearn

from config import iot23_experiments_dir
from src.experiments import data_combinations, feature_combinations
from src.helpers.file_helper import list_folder_names
from src.helpers.log_helper import add_logger
from src.helpers.report_helper import combine_reports
from src.helpers.model_stats_helper import explore_experiments_results


# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

add_logger(file_name='06_explore_exp_results.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Setup warnings
# warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
# warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)
# np.seterr(divide='ignore', invalid='ignore')

# Explore data
exp_home_dir = iot23_experiments_dir
data_combinations = [
    # data_combinations['S13_R_100_000'],  # 10 sec
    # data_combinations['S13_R_5_000_000'],  # 30 sec
    # data_combinations['S04_R_5_000_000'],  # 30 sec
    data_combinations['S16_R_5_000_000'],  # 30 sec
]

# Selected Features
feature_combos = [
    feature_combinations['F14'],
    # feature_combinations['F17'],
    # feature_combinations['F18'],
    # feature_combinations['F19'],
]

explore_experiments_results(exp_home_dir,
                            data_combinations,
                            feature_combos,
                            enable_score_tables=True,
                            enable_score_charts=True,
                            enable_model_insights=False)

# Combine reports
exp_dir = iot23_experiments_dir
exp_list_all = list_folder_names(exp_dir)
combine_reports(exp_dir, exp_list_all, 'all_improved.xlsx')

print('Step 06: The end.')
quit()
