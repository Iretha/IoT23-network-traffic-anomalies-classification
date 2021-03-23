from glob import glob
import logging
import time
import re
import os.path
from os import path
from random import shuffle
from pathlib import Path
from os import walk
import json

from src.helpers.log_helper import log_duration


def mk_dir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def combine_files(source_dir,
                  source_file_names,
                  output_dir,
                  output_file_name,
                  header_line=None,
                  max_rows_from_file=None,
                  skip_rows=None):
    if len(source_file_names) == 0:
        _, _, filenames = next(walk(source_dir))
        source_file_names = filenames

    source_files = []
    for source_file_name in source_file_names:
        source_files.append(source_dir + source_file_name)
    target_file_path = output_dir + output_file_name
    combine_files_content(source_files, target_file_path, header_line=header_line, max_rows_from_file=max_rows_from_file, skip_rows=skip_rows)


def combine_files_content(source_files,
                          target_file_path,
                          header_line=None,
                          max_rows_from_file=None,
                          skip_rows=None,
                          extract_header_row=None,
                          delete_source_file=False):
    logging.info("-----> Mix data from multiple files: " + str(len(source_files)))
    start_time = time.time()

    shuffle(source_files)

    if header_line is None and extract_header_row:
        with open(source_files[0], "r+") as source_header_file:
            for line in source_header_file:
                header_line = line
                break

    file_counter = 0
    with open(target_file_path, "w+") as target_file:
        if header_line is not None:
            target_file.write(header_line)
        for file_path in source_files:
            file_counter += 1
            logging.info(str(file_counter) + '. Read data from file: ' + file_path)
            write_file_content(file_path, target_file, max_rows_from_file=max_rows_from_file, skip_rows=skip_rows)
            if delete_source_file:
                os.remove(file_path)
                logging.info("Deleting file: " + file_path)

    log_duration(start_time, '-----> Mixing data finished in')


def write_file_content(source_file_path,
                       target_file,
                       max_rows_from_file=None,
                       skip_rows=0):
    file_start_time = time.time()
    row_counter = 0
    with open(source_file_path, "r") as source_file:
        for line in source_file:
            if skip_rows > 0:
                skip_rows -= 1
                continue

            if is_not_comment(line):
                target_file.write(line)
                row_counter += 1
                if max_rows_from_file == row_counter:
                    break
    exec_time = time.time() - file_start_time
    logging.info('End reading data from file in %s seconds = %s minutes, current row count is %s ...' % (exec_time, (exec_time / 60), row_counter))


def split_files_by_value_in_col(dataset_location,
                                file_name_pattern,
                                output_dir,
                                header_line,
                                column_index=22,
                                sep='\s+',
                                max_size_in_mb=None):
    logging.info("--> Start splitting file . . . ")
    start_time = time.time()

    source_files = find_files_recursively(dataset_location, file_name_pattern)
    source_files = filter_out_files_larger_than(source_files, max_size_in_mb=max_size_in_mb)
    logging.info(str(len(source_files)) + " files to process ")

    map_key_values = {'-': 'Benign'}
    file_counter = 0
    file_cache = {}
    for file_path in source_files:
        file_counter += 1
        logging.info(str(file_counter) + '. Start processing file: ' + file_path)
        file_start_time = time.time()
        with open(file_path, "r") as source_file:
            for line in source_file:
                if is_not_comment(line):
                    value = get_col_value(line, sep, column_index, map_key_values=map_key_values)
                    output_file_exists = True if value in file_cache else False
                    if output_file_exists:
                        target_file = file_cache[value]
                    else:
                        output_file = output_dir + value + '.csv'
                        target_file = open(output_file, "a+")
                        target_file.write(header_line)
                        file_cache[value] = target_file
                    target_file.write(line)
        file_end_time = time.time()
        logging.info('End processing file in %s seconds = %s minutes...' % (
            (file_end_time - file_start_time), ((file_end_time - file_start_time) / 60)))

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("---> END in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def find_files_recursively(location_dir, file_name_pattern):
    pathname = location_dir + file_name_pattern
    files = glob(pathname, recursive=True)

    logging.info('Files found: ' + str(len(files)))
    return files


def filter_out_files_larger_than(file_paths=[], max_size_in_mb=None):
    if max_size_in_mb is None:
        return file_paths

    filtered_files = []
    for idx in range(len(file_paths)):
        file = file_paths[idx]
        file_size_in_mb = get_file_size_in_mb(file)
        if 0 < max_size_in_mb < file_size_in_mb:
            logging.info('File is too large, so it will be skipped: ' + file)
        else:
            filtered_files.append(file)
    return filtered_files


def get_file_size_in_mb(file_path):
    file_exists = path.exists(file_path)
    size_in_mb = -1
    if file_exists:
        size_in_bytes = os.path.getsize(file_path)
        size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb


def get_file_size_in_gb(file_path):
    size_in_mb = get_file_size_in_mb(file_path)
    return size_in_mb / 1000


def get_col_value(line, sep, idx, map_key_values={}):
    cols = re.split(sep, line)
    val = (cols[idx]).strip()
    return map_key_values.get(val, val)


def is_not_comment(line):
    return not line.startswith('#')  # skip commented lines


def shuffle_file_content(source_dir, source_file_name):
    logging.info("-----> Shuffle content rows . . . ")
    start_time = time.time()

    source_file_path = source_dir + source_file_name
    output_file_path = source_file_path + '_tmp.csv'
    with open(source_file_path, 'r') as ip:
        data = ip.readlines()
        header, rest = data[0], data[1:]
        shuffle(rest)
        with open(output_file_path, 'w') as out:
            out.write(''.join([header] + rest))

    overwrite_existing_file(source_file_path, output_file_path)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("-----> Shuffle finished in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def overwrite_existing_file(source_file_path, output_file_path):
    os.remove(source_file_path)
    os.rename(output_file_path, source_file_path)


def list_folder_names(parent_dir):
    file_paths = glob(parent_dir + "/*/")
    dirs = []
    for p in file_paths:
        dir_name = os.path.dirname(p)
        dir_name = os.path.split(dir_name)[-1]
        dirs.append(dir_name)
    return dirs


def write_json_file(output_path, data):
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile)


def delete_dir_content(iot23_output_directory):
    files = glob(iot23_output_directory + '/*')
    for f in files:
        os.remove(f)

    logging.info('Content of ' + iot23_output_directory + ' is deleted.')
