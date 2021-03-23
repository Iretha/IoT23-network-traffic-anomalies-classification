import logging

from config import iot23_attacks_dir, iot23_scenarios_dir
from src.iot23 import iot23_metadata
from src.helpers.file_helper import delete_dir_content
from src.helpers.log_helper import add_logger
from src.helpers.scenario_helper import split_scenarios_by_label

# Add Logger
add_logger(file_name='01_extract_data.log')
logging.warning("!!! This step takes about 120 min to complete !!!")

# Delete existing files in target dir
output_dir = iot23_attacks_dir
delete_dir_content(output_dir)

# Split scenarios
source_dir = iot23_scenarios_dir
file_name_pattern = iot23_metadata['file_name_pattern']
header_line = iot23_metadata['file_header']
split_scenarios_by_label(source_dir,
                         file_name_pattern,
                         output_dir,
                         header_line)

print('Step 01: The End')
quit()
