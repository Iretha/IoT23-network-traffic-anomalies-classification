import logging
import pandas as pd
from os import path
import sys
import time

from sklearn.preprocessing import OrdinalEncoder


def df_get(file_path, delimiter='\t', header=0):
    logging.debug('Load data file: ' + file_path)
    return pd.read_csv(file_path, delimiter=delimiter, header=header)


def df_transform_to_numeric(df, columns=None):
    if columns is None or len(columns) == 0:
        columns = list(df.select_dtypes(include=['object']).columns)

    logging.info('Transform columns to numeric: ' + ', '.join(columns))
    for column_name in columns:
        df[column_name] = pd.to_numeric(df[column_name], errors='ignore')

    return df


def df_encode_objects(df):
    ord_enc = OrdinalEncoder()
    obj_column_names = list(df.select_dtypes(include=['object']).columns)
    logging.info('Encode object columns: ' + ', '.join(obj_column_names))
    for obj_column_name in obj_column_names:
        try:
            df[obj_column_name] = ord_enc.fit_transform(df[[obj_column_name]])
        except:
            logging.error("Oops! Could not transform values in col= " + obj_column_name, sys.exc_info()[0])


# TODO two save-s
def save_to_csv(df, dest_dir, file_name, append=False):
    mode = 'w' if append is False else 'a'
    df.to_csv(dest_dir + file_name, index=False, mode=mode)
    logging.info('Save file: ' + file_name)


# TODO two save-s, use one
def write_to_csv(df, dest_file_path, mode='a'):
    add_header = False if (mode == 'a' and path.exists(dest_file_path)) else True
    df.to_csv(dest_file_path, mode=mode, header=add_header, index=False)
    logging.info('File saved: ' + dest_file_path)


def scale_data(x_data, scaler):
    logging.info("-----> Scale data . . . ")
    start_time = time.time()

    scaler.fit(x_data)
    x_data = scaler.transform(x_data)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Data scaled in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return x_data


def load_data_into_frame(data_file_path, classification_col_name, columns=None, scaler=None):
    # Load data in df
    df = df_get(data_file_path, delimiter=',')

    # Select columns
    if columns is None or len(columns) == 0:
        columns = list(df.columns)

    # Select features
    selected_features = [x for x in columns if x not in [classification_col_name]]
    y = df[classification_col_name]
    x = df[selected_features]

    # Scale data
    if scaler is not None:
        x = scale_data(x, scaler)

    return x, y


def load_data(file_path, classification_col_name, features=None, scaler=None):
    if features is None:
        features = []
    logging.info("-----> Load data ")
    start_time = time.time()

    # Load data
    x, y = load_data_into_frame(file_path, classification_col_name, columns=features, scaler=scaler)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Data loaded in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
    return x, y
