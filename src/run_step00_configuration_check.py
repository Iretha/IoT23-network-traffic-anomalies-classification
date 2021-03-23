from config import iot23_scenarios_dir, iot23_attacks_dir, iot23_experiments_dir, iot23_data_dir
from src.iot23 import iot23_metadata
from src.helpers.config_helper import check_config
from src.helpers.log_helper import add_logger

# Add Logger
add_logger(file_name='00_config_check.log')

# Check Config
scenarios_location = iot23_scenarios_dir
file_name_pattern = iot23_metadata['file_name_pattern']
attack_files_location = iot23_attacks_dir
data_dir = iot23_data_dir
experiments_location = iot23_experiments_dir
check_config(scenarios_location,
             file_name_pattern,
             attack_files_location,
             data_dir,
             experiments_location)

print('Step 00: The End')
quit()
