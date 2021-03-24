import logging
from config import iot23_experiments_dir
from src.iot23 import feature_selections, get_data_sample
from src.helpers.log_helper import add_logger
from src.helpers.data_stats_helper import explore_experiments_train_test_data

add_logger(file_name='05_explore_exp_data.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Explore data
exp_home_dir = iot23_experiments_dir
data_samples = [
    get_data_sample(dataset_name='S04', rows_per_dataset_file=100_000),
    get_data_sample(dataset_name='S16', rows_per_dataset_file=100_000),
    #
    # get_data_sample(dataset_name='S04', rows_per_dataset_file=5_000_000),
    # get_data_sample(dataset_name='S16', rows_per_dataset_file=5_000_000),
]

# Selected Features
features = [
    feature_selections['F14'],
    # feature_selections['F17'],
    # feature_selections['F18'],
    # feature_selections['F19'],
]

explore_experiments_train_test_data(exp_home_dir,
                                    data_samples,
                                    features,
                                    plot_corr=True,
                                    plot_cls_dist=True,
                                    plot_attr_dist=True)

print('Step 05: The end.')
quit()
