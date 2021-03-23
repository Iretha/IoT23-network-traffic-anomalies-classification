import logging

from config import iot23_attacks_dir, iot23_data_dir
from src.iot23 import iot23_metadata, data_samples, data_cleanup
from src.helpers.log_helper import add_logger
from src.helpers.data_helper import prepare_data

# Add Logger
add_logger(file_name='02_prepare_data.log')
logging.warning("!!! This step takes about 20 min to complete !!!")

# Prepare data
source_files_dir = iot23_attacks_dir
output_files_dir = iot23_data_dir
combinations = [
    data_samples['S16-DEMO_R_100_000'],  # 10 sec

    # data_samples['S04_R_5_000_000'],  # 30 sec
    # data_samples['S16_R_5_000_000'],  # 30 sec
]
prepare_data(source_files_dir,
             output_files_dir,
             iot23_metadata["file_header"],
             data_cleanup,
             data_combinations=combinations,
             overwrite=False)

print('Step 02: The end.')
quit()
