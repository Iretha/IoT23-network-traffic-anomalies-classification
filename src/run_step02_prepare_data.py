import logging

from config import iot23_attacks_dir, iot23_data_dir
from src.iot23 import iot23_metadata, data_cleanup, get_data_sample
from src.helpers.log_helper import add_logger
from src.helpers.data_helper import run_data_preprocessing

# Add Logger
add_logger(file_name='02_prepare_data.log')
logging.warning("!!! This step takes about 20 min to complete !!!")

# Prepare data
source_files_dir = iot23_attacks_dir
output_files_dir = iot23_data_dir

data_samples = [
    get_data_sample(dataset_name='S04', rows_per_dataset_file=5_000_000),  # ~ 10 min
    get_data_sample(dataset_name='S16', rows_per_dataset_file=5_000_000),  # ~ 10 min
]
run_data_preprocessing(source_files_dir,
                       output_files_dir,
                       iot23_metadata["file_header"],
                       data_cleanup,
                       data_samples=data_samples,
                       overwrite=False)

print('Step 02: The end.')
quit()
