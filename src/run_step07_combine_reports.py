import logging
from config import iot23_experiments_dir
from src.helpers.file_helper import list_folder_names
from src.helpers.log_helper import add_logger
from src.helpers.report_helper import combine_reports

add_logger(file_name='07_combine_results.log')
logging.warning("!!! This step takes about 3 min to complete !!!")

# Combine reports
exp_dir = iot23_experiments_dir
exp_list_all = list_folder_names(exp_dir)
combine_reports(exp_dir, exp_list_all, 'all.xlsx')

print('Step 07: The end.')
quit()
