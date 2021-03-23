import logging
from config import iot23_experiments_dir
from src.iot23 import data_samples, feature_selections
from src.helpers.log_helper import add_logger
from src.helpers.data_stats_helper import explore_experiments_data

add_logger(file_name='05_explore_exp_data.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Explore data
exp_home_dir = iot23_experiments_dir
data_combinations = [
    data_samples['S16-DEMO_R_100_000'],  # 10 sec

    # data_samples['S04_R_5_000_000'],  # 30 sec
    # data_samples['S16_R_5_000_000'],  # 30 sec
]

# Selected Features
features = [
    feature_selections['F14'],
    # feature_selections['F17'],
    # feature_selections['F18'],
    # feature_selections['F19'],
]

explore_experiments_data(exp_home_dir,
                         data_combinations,
                         features,
                         plot_corr=True,
                         plot_cls_dist=True,
                         plot_attr_dist=True)

print('Step 05: The end.')
quit()
