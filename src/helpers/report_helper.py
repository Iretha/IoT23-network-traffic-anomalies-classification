import os
import logging
import json
import time

from src.helpers.file_helper import find_files_recursively
from src.helpers.log_helper import log_duration
from src.helpers.xls_helper import export_stats_xls


def combine_reports(exp_dir,
                    experiment_names,
                    output_file_name):
    logging.info("===== Combine stats: " + str(experiment_names))
    start_time = time.time()

    json_stats = __find_json_stats(exp_dir, experiment_names)
    export_stats_xls(exp_dir, json_stats, output_file_name=output_file_name)

    log_duration(start_time, "===== Stats combined in")


def __find_json_stats(exp_dir, experiment_names):
    logging.info("===== Load json files: ")
    start_time = time.time()

    json_stats = {}
    for experiment_name in experiment_names:
        json_files = find_files_recursively(exp_dir + experiment_name + '\\results\\', '\*_scores.json')
        for json_file_path in json_files:
            if os.path.exists(json_file_path):
                with open(json_file_path) as json_file:
                    json_stats[experiment_name] = json.load(json_file)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Json files loaded in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

    return json_stats
