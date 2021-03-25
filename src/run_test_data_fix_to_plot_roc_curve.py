import pandas as pd
from numpy import sort

from config import iot23_experiments_dir
from src.helpers.dataframe_helper import df_get, write_to_csv
from src.helpers.file_helper import find_files_recursively
from src.iot23 import get_exp_data_dir, get_train_data_path, get_test_data_path


def add_missing_classes(train_data_path, test_data_path):
    if train_data_path is None or test_data_path is None:
        return

    df_train = df_get(train_data_path, delimiter=',')
    train_classes = sort(list(df_train['detailed-label'].unique()))

    df_test = df_get(test_data_path, delimiter=',')
    test_classes = sort(list(df_test['detailed-label'].unique()))

    classes_missing_in_test = sort(list(set(train_classes) - set(test_classes)))
    copy_random_record_of_class(df_train, df_test, test_data_path, classes_missing_in_test)


def copy_random_record_of_class(from_df, to_df, to_file_path, classes=None):
    if classes is None or len(classes) == 0:
        return

    print('Missing classes: ' + str(classes) + ' in ' + to_file_path)
    cnt = 0
    for clz in classes:
        sample_df = from_df[from_df['detailed-label'] == clz].sample(1)
        to_df = to_df.append(sample_df)
        cnt += 1

    if cnt > 0:
        write_to_csv(to_df, to_file_path, mode='w')


def fix_test_data_to_plot_roc_curve(exp_parent_dir, exp_folders):
    for exp_folder in exp_folders:
        data_dir = get_exp_data_dir(exp_parent_dir + exp_folder)
        train_file_path = get_data_file(data_dir, get_train_data_path(''))
        test_file_path = get_data_file(data_dir, get_test_data_path(''))
        add_missing_classes(train_file_path, test_file_path)


def get_data_file(folder, file_name_ends_with):
    files = find_files_recursively(folder, '/*' + file_name_ends_with)
    return files[0] if len(files) > 0 else None


pd.set_option('display.max_row', 100)
pd.set_option('display.max_columns', 50)

experiments_dir = iot23_experiments_dir
experiments_to_fix = [
    'F14_S16_R_5_000_000',
    'F17_S16_R_5_000_000',
    'F18_S16_R_5_000_000',
    'F19_S16_R_5_000_000',
]

fix_test_data_to_plot_roc_curve(experiments_dir, experiments_to_fix)
print('The end.')
