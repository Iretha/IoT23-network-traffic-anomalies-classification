import logging
from config import iot23_data_dir
from src.iot23 import get_data_sample
from src.helpers.data_stats_helper import explore_clean_data
from src.helpers.log_helper import add_logger

# Add Logger
add_logger(file_name='03_explore_data.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Selected Data Files
data_file_dir = iot23_data_dir
data_samples = [
    get_data_sample(dataset_name='S04', rows_per_dataset_file=5_000_000),
    get_data_sample(dataset_name='S16', rows_per_dataset_file=5_000_000),
]
explore_clean_data(data_file_dir,
                   data_samples=data_samples,
                   plot_corr=True,
                   plot_cls_dist=True,
                   plot_attr_dist=True)

print('Step 03: The end.')
quit()
