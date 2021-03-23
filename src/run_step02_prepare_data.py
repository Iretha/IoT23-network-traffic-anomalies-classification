import logging

from config import iot23_attacks_dir, iot23_data_dir
from src.experiments import iot23_config, data_combinations, data_cleanup_conf
from src.helpers.log_helper import add_logger
from src.helpers.data_helper import prepare_data

# Add Logger
add_logger(file_name='02_prepare_data.log')
logging.warning("!!! This step takes about 20 min to complete !!!")

# Prepare data
source_files_dir = iot23_attacks_dir
output_files_dir = iot23_data_dir
combinations = [
    # data_combinations['S13_R_100_000'],  # 10 sec
    # data_combinations['S13_R_5_000_000'],  # 30 sec
    # data_combinations['S04_R_5_000_000'],  # 30 sec
    data_combinations['S16_R_5_000_000'],  # 30 sec

]
prepare_data(source_files_dir,
             output_files_dir,
             iot23_config["file_header"],
             data_cleanup_conf,
             data_combinations=combinations,
             overwrite=False)

print('Step 02: The end.')
quit()
