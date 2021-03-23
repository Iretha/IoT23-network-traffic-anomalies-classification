import logging
from config import iot23_data_dir
from src.iot23 import data_samples, feature_selections
from src.helpers.data_stats_helper import explore_data_combinations
from src.helpers.log_helper import add_logger

# Add Logger
add_logger(file_name='03_explore_data.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Selected Data Files
data_file_dir = iot23_data_dir
data_combinations = [
    data_samples['S16-DEMO_R_100_000'],  # 10 sec

    # data_samples['S04_R_5_000_000'],  # 30 sec
    # data_samples['S16_R_5_000_000'],  # 30 sec
]
explore_data_combinations(data_file_dir,
                          combinations=data_combinations,
                          plot_corr=True,
                          plot_cls_dist=True,
                          plot_attr_dist=True)

print('Step 03: The end.')
quit()
