import os
import logging
import json
import time
from src.helpers.log_helper import log_duration
from src.iot23 import get_test_data_path, get_train_data_path
from src.helpers.dataframe_helper import df_get, load_data
from src.helpers.file_helper import mk_dir
from src.helpers.plt_helper import plot_correlations, plot_class_values_distribution, plot_attr_values_distribution
from src.helpers.model_stats_helper import export_model_stats
from src.helpers.xls_helper import export_stats_xls


def run_reports(exp_dir,
                experiment_names,
                data_file_name,
                classification_col_name,
                export_data_charts=False,
                export_score_tables=True,
                export_score_charts=False):
    for experiment_name in experiment_names:
        __run_report(exp_dir,
                     experiment_name,
                     data_file_name,
                     classification_col_name,
                     export_data_charts=export_data_charts,
                     export_score_tables=export_score_tables,
                     export_score_charts=export_score_charts)


def __run_report(experiments_dir,
                 experiment_name,
                 data_file,
                 class_col_name,
                 results_dir='results',
                 export_data_charts=False,
                 export_score_tables=True,
                 export_score_charts=False):
    if not export_data_charts and not export_score_tables and not export_score_charts:
        return

    logging.info("===== Export stats: " + experiment_name)
    start_time = time.time()

    # Make stats directory
    experiment_location = experiments_dir + experiment_name + "\\"
    results_path = experiment_location + results_dir + "\\"
    mk_dir(results_path)

    # Load data
    data_file_path = experiment_location + "\\data\\" + data_file
    x_test, y_test = load_data(get_test_data_path(data_file_path), class_col_name)

    # Export Data Charts
    __export_data_stats(experiment_name,
                        data_file_path,
                        results_path,
                        class_col_name,
                        export_data_charts=export_data_charts)
    logging.info("****** Data charts are in " + results_path)

    # Export Model Scores
    models_dir = experiment_location + "\\models\\"
    export_model_stats(experiment_name,
                       models_dir,
                       x_test,
                       y_test,
                       results_path,
                       class_col_name,
                       export_score_tables=export_score_tables,
                       export_score_charts=export_score_charts)
    logging.info("****** Model stats & charts are in " + results_path)

    log_duration(start_time, "===== Stats " + experiment_name + " exported in")


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
        experiment_result_json = exp_dir + experiment_name + '\\results\\stats.json'
        if os.path.exists(experiment_result_json):
            with open(experiment_result_json) as json_file:
                json_stats[experiment_name] = json.load(json_file)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Json files loaded in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))

    return json_stats


def __export_data_stats(experiment_name,
                        source_file_path,
                        results_path,
                        class_col_name,
                        export_data_charts=False):
    if not export_data_charts:
        return

    # Data Stats
    df = df_get(source_file_path, delimiter=',')
    __export_data_chart_images(experiment_name,
                               results_path,
                               class_col_name,
                               df,
                               prefix=experiment_name + 'data_',
                               export=True)

    # Train Data Stats
    df_train = df_get(get_train_data_path(source_file_path), delimiter=',')
    __export_data_chart_images(experiment_name,
                               results_path,
                               class_col_name,
                               df_train,
                               prefix=experiment_name + 'data_train_',
                               export=True)

    # Test Data Stats
    df_test = df_get(get_test_data_path(source_file_path), delimiter=',')
    __export_data_chart_images(experiment_name,
                               results_path,
                               class_col_name,
                               df_test,
                               prefix=experiment_name + '_data_test_',
                               export=True)


def __export_data_chart_images(experiment_name,
                               stats_location,
                               class_col_name,
                               df,
                               prefix='',
                               export=True):
    plot_correlations(stats_location,
                      df.corr(),
                      title='\n' + experiment_name + '\n\n' + "Correlations",
                      file_name=prefix + "_correlations.png",
                      export=export)

    plot_class_values_distribution(stats_location,
                                   df,
                                   class_col_name,
                                   title='\n' + experiment_name + '\n\n' + "Class Frequency",
                                   file_name=prefix + "class_values_distribution.png",
                                   export=export)

    plot_attr_values_distribution(stats_location,
                                  df,
                                  title='\n' + experiment_name + '\n\n' + "Attribute Distribution",
                                  file_name=prefix + "attr_distribution.png",
                                  export=export)
