import logging

from src.helpers.log_helper import add_logger
from src.helpers.shuffle_content_helper import shuffle_files_content

# Add Logger
add_logger(file_name='01_extract_data.log')
logging.warning("!!! This step takes about 120 min to complete !!!")

source_files_dir = 'E:\\machine-learning\\datasets\\iot23\\2_attacks\\'
source_files_pattern = source_files_dir + "*.csv"

shuffle_files_content(source_files_pattern)

# shuffle_file_in_partitions('E:\\machine-learning\\datasets\\iot23\\2_attacks\\DDoS.csv', partitions_per_gb=1)

print('The end')
quit()
