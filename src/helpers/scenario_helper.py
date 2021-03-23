import logging
import time

from src.experiments import format_line
from src.helpers.file_helper import find_files_recursively, filter_out_files_larger_than, is_not_comment, get_col_value
from src.helpers.log_helper import log_duration


def split_scenarios_by_label(dataset_location,
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
                        target_file.write(format_line(header_line))
                        file_cache[value] = target_file
                    target_file.write(format_line(line))
        file_end_time = time.time()
        logging.info('End processing file in %s seconds = %s minutes...' % (
            (file_end_time - file_start_time), ((file_end_time - file_start_time) / 60)))

    log_duration(start_time, '---> END in')
