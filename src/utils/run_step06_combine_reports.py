import logging

from numpy import sort

from config import iot23_experiments_dir
from src.helpers.file_helper import list_folder_names
from src.helpers.log_helper import add_logger
from src.helpers.report_helper import combine_reports

add_logger(file_name='07_combine_results.log')
logging.warning("!!! This step takes about 0 min to complete !!!")

# Combine reports
exp_dir = iot23_experiments_dir
exp_list_all = sort(list_folder_names(exp_dir))
combine_reports(exp_dir, exp_list_all, 'S04_S16_all_scores.xlsx')

print('Step 06: The end.')
quit()
