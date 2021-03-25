import os
import logging
import json
import time
from src.helpers.xls_helper import export_stats_xls


def combine_reports(exp_dir,
                    experiment_names,
                    output_file_name):
    logging.info("===== Combine stats: " + str(experiment_names))
    start_time = time.time()

    json_stats = __find_json_stats(exp_dir, experiment_names)
    export_stats_xls(exp_dir, json_stats, output_file_name=output_file_name, enable_score_tables=True)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Stats combined in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def __find_json_stats(exp_dir, experiment_names):
    logging.info("===== Load json files: ")
    start_time = time.time()

    json_stats = {}
    for experiment_name in experiment_names:
        experiment_result_json = exp_dir + experiment_name + '\\results\\*_scores.json'
        if os.path.exists(experiment_result_json):
            with open(experiment_result_json) as json_file:
                json_stats[experiment_name] = json.load(json_file)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Json files loaded in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

    return json_stats
