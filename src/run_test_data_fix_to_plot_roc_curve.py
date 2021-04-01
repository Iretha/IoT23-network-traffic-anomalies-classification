import pandas as pd

from config import iot23_experiments_dir
from src.helpers.file_helper import find_files_recursively
from src.helpers.fix_test_data_for_roc import add_missing_class_rows_to_test_data
from src.iot23 import get_exp_data_dir, get_train_data_path, get_test_data_path


def fix_test_data_to_plot_roc_curve(exp_parent_dir, exp_folders):
    for exp_folder in exp_folders:
        data_dir = get_exp_data_dir(exp_parent_dir + exp_folder)
        train_file_path = get_data_file(data_dir, get_train_data_path(''))
        test_file_path = get_data_file(data_dir, get_test_data_path(''))
        add_missing_class_rows_to_test_data(train_file_path, test_file_path)


def get_data_file(folder, file_name_ends_with):
    files = find_files_recursively(folder, '/*' + file_name_ends_with)
    return files[0] if len(files) > 0 else None


pd.set_option('display.max_row', 100)
pd.set_option('display.max_columns', 50)

# experiments_dir = iot23_experiments_dir
# experiments_to_fix = [
#     'F14_S16_R_5_000_000',
#     'F17_S16_R_5_000_000',
#     'F18_S16_R_5_000_000',
#     'F19_S16_R_5_000_000',
# ]
#
# fix_test_data_to_plot_roc_curve(experiments_dir, experiments_to_fix)

file_dir = 'E:\\machine-learning\\datasets\\iot23\\3_data_v2\\'
train_file_path = file_dir + 'S04_R_5_000_000_clean.csv_train.csv'
test_file_path = file_dir + 'S04_R_5_000_000_clean.csv_test.csv'
add_missing_class_rows_to_test_data(train_file_path, test_file_path)
print('The end.')
