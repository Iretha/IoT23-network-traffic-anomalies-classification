import glob
import logging
import os
from random import shuffle, randint
import time

from src.helpers.file_helper import get_file_size_in_gb, combine_files_content
from src.helpers.log_helper import log_duration


def shuffle_files_content(files_pattern, overwrite=True):
    source_files = glob.glob(files_pattern)
    for source_file in source_files:
        shuffle_file_in_partitions(source_file, partitions_per_gb=1, overwrite=overwrite)


def shuffle_file_in_partitions(source_file_path, partitions_per_gb=1, overwrite=True):
    logging.info("====> Start processing " + source_file_path)
    start_time = time.time()

    output_file_path = source_file_path + '.rnd'
    exists = os.path.exists(output_file_path)
    if exists:
        logging.info("====> File already processed. Skipping... ")
        return

    # Calculate partitions count
    curr_size_in_gb = max(1, round(get_file_size_in_gb(source_file_path)))
    partitions_count = round(curr_size_in_gb / partitions_per_gb)

    # Partition file
    __partition_file(source_file_path, partitions_count, part_ext='.part.')

    # List partitions
    partitions = __list_file_partitions(source_file_path, part_ext_pattern='.part.*')

    # Shuffle partition content
    for partition in partitions:
        __shuffle_partition_content(partition, tmp_ext='.tmp', overwrite=True)

    # Combine partitions
    output_file_path = source_file_path + '.rnd'
    combine_files_content(partitions, output_file_path, skip_rows=1, extract_header_row=True, delete_source_file=True)

    # Overwrite file
    if overwrite:
        __overwrite_existing_file(source_file_path, output_file_path)

    log_duration(start_time, '====> File processed in ')


def __partition_file(source_file_path, partitions_count, part_ext='.part.'):
    logging.info('---> Partition ' + source_file_path + ' into ' + str(partitions_count) + ' partitions!')
    start_time = time.time()

    source_row_no = 0
    header_line = None
    file_cache = {}
    file_paths = []

    try:
        with open(source_file_path, "r") as source_file:
            for line in source_file:
                if source_row_no == 0:
                    header_line = line
                    source_row_no += 1
                else:
                    rnd_file_no = randint(1, partitions_count)
                    output_file_exists = True if rnd_file_no in file_cache else False
                    if output_file_exists:
                        target_file = file_cache[rnd_file_no]
                    else:
                        output_file = source_file_path + part_ext + str(rnd_file_no)
                        target_file = open(output_file, "a+")
                        target_file.write(header_line)
                        file_cache[rnd_file_no] = target_file
                        file_paths.append(output_file)
                    target_file.write(line)
    finally:
        for key in file_cache:
            try:
                file_cache[key].close()
            except:
                logging.warning("File could not be closed.")

    log_duration(start_time, 'Partitioning ended in ')
    return file_paths


def __list_file_partitions(source_file_path, part_ext_pattern='.part.*'):
    partitions_pattern = source_file_path + part_ext_pattern
    partitions = glob.glob(partitions_pattern)
    return partitions


def __shuffle_partition_content(source_file_path, tmp_ext='.tmp', overwrite=False):
    logging.info("-----> Shuffle content rows of " + source_file_path)
    start_time = time.time()

    output_file_path = source_file_path + tmp_ext
    exists = os.path.exists(output_file_path)

    if not exists:
        with open(source_file_path, 'r') as ip:
            data = ip.readlines()
            header, rest = data[0], data[1:]
            shuffle(rest)
            with open(output_file_path, 'w') as out:
                out.write(''.join([header] + rest))

            try:
                out.close()
            except:
                logging.warning("Could not close file: " + output_file_path)
        log_duration(start_time, '----> Content shuffled in ')

        if overwrite:
            __overwrite_existing_file(source_file_path, output_file_path)


def __overwrite_existing_file(source_file_path, output_file_path):
    os.remove(source_file_path)
    os.rename(output_file_path, source_file_path)
