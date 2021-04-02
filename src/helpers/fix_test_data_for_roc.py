from numpy import sort
from src.helpers.dataframe_helper import df_get, write_to_csv


def add_missing_class_rows_to_test_data(train_data_path, test_data_path):
    __add_missing_classes(train_data_path, test_data_path)


def __add_missing_classes(train_data_path, test_data_path):
    if train_data_path is None or test_data_path is None:
        return

    df_train = df_get(train_data_path, delimiter=',')
    train_classes = sort(list(df_train['detailed-label'].unique()))

    df_test = df_get(test_data_path, delimiter=',')
    test_classes = sort(list(df_test['detailed-label'].unique()))

    classes_missing_in_test = sort(list(set(train_classes) - set(test_classes)))
    __copy_random_record_of_class(df_train, train_data_path, df_test, test_data_path, classes_missing_in_test)


def __copy_random_record_of_class(from_df, from_file_path, to_df, to_file_path, classes=None):
    """
    TODO if we want to be more precise, we have to move the row, not just copy it
    """
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
