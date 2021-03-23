import glob
import os
import re
import ntpath
import logging
import json
import time
import psutil

from sklearn.metrics import classification_report

from src.experiments import get_test_data_path, get_train_data_path
from src.helpers.dataframe_helper import df_get, load_data
from src.helpers.file_helper import mk_dir, write_json_file
from src.helpers.model_helper import load_model
from src.helpers.plt_helper import plot_correlations, plot_class_values_distribution, plot_attr_values_distribution, \
    plot_model_precision_recall_curve, plot_confusion_ma3x, plot_feature_importance, plot_permutation_importance, plot_model_roc_curve
from src.helpers.model_stats_helper import score_model
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
    __export_model_stats(experiment_name,
                         models_dir,
                         x_test,
                         y_test,
                         results_path,
                         class_col_name,
                         export_score_tables=export_score_tables,
                         export_score_charts=export_score_charts)
    logging.info("****** Model stats & charts are in " + results_path)

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Stats " + experiment_name + " exported in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


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


def __export_model_stats(experiment_name,
                         models_location,
                         x_test,
                         y_test,
                         results_location,
                         class_col_name,
                         export_score_tables=True,
                         export_score_charts=False):
    if not export_score_tables and not export_score_charts:
        return

    stats = {}
    model_stats = {}
    pid = os.getpid()
    p = psutil.Process(pid)
    # Score
    model_paths = glob.glob(models_location + "/*.pkl")
    for model_path in model_paths:
        model_name = ntpath.basename(model_path)
        model_name = re.findall(r'[^\/]+(?=\.)', model_name)[0]
        # print(p.memory_info())
        # print(p.cpu_percent(interval=1.0))
        model = load_model(model_path)
        if model is not None:
            # print(p.memory_info())
            # print(p.cpu_percent(interval=1.0))
            y_test, predictions, adv_stats = score_model(model_name,
                                                         model,
                                                         x_test,
                                                         y_test)
            model_stats[model_name] = __prepare_model_stats(y_test,
                                                            predictions,
                                                            adv_stats,
                                                            export_score_tables=export_score_tables)
            __export_model_chart_images(results_location,
                                        model_name, model,
                                        x_test,
                                        y_test,
                                        predictions,
                                        experiment_name,
                                        adv_stats,
                                        export_score_charts=export_score_charts)

    stats['model_stats'] = model_stats
    write_json_file(results_location + 'stats.json', stats)
    export_stats_xls(results_location,
                     {experiment_name: stats},
                     output_file_name=experiment_name + '.xlsx',
                     enable_score_tables=export_score_tables)


def __prepare_model_stats(y_true, y_pred, adv_stats, export_score_tables=False):
    if not export_score_tables:
        return

    return {'classification_report': classification_report(y_true, y_pred, output_dict=True),
            'adv_stats': adv_stats}


def __export_model_chart_images(results_location,
                                model_name,
                                model,
                                x_test,
                                y_test,
                                y_pred,
                                experiment_name,
                                adv_stats,
                                export_score_charts=False):
    if not export_score_charts:
        return

    if adv_stats is not None:
        if 'Feature Importance' in adv_stats:
            feat_imp = adv_stats['Feature Importance']
            if feat_imp is not None:
                plot_feature_importance(results_location,
                                        model_name,
                                        experiment_name,
                                        feat_imp,
                                        title=experiment_name + "\n\n" + model_name + "\nFeature Importance",
                                        file_name=experiment_name + '_' + model_name + "_feat_imp.png")
        if 'Permutation Importance' in adv_stats:
            imp = adv_stats['Permutation Importance']
            if imp is not None:
                plot_permutation_importance(results_location,
                                            model_name,
                                            experiment_name,
                                            imp,
                                            title=experiment_name + "\n\n" + model_name + "\nPermutation Importance",
                                            file_name=experiment_name + '_' + model_name + "_permutation_imp.png")

    plot_confusion_ma3x(results_location,
                        y_test,
                        y_pred,
                        experiment_name,
                        title=experiment_name + "\n\n" + model_name + "\nConfusion Matrix",
                        file_name=experiment_name + '_' + model_name + "_conf_m3x.png")

    plot_model_roc_curve(results_location,
                         model,
                         model_name,
                         x_test,
                         y_test,
                         experiment_name,
                         title=experiment_name + "\n\n" + model_name + "\nROC Curves",
                         file_name=experiment_name + '_' + model_name + "_roc_curve.png")

    plot_model_precision_recall_curve(results_location,
                                      model,
                                      model_name,
                                      x_test,
                                      y_test,
                                      experiment_name,
                                      title=experiment_name + "\n\n" + model_name + "\nPrecision-Recall Curves",
                                      file_name=experiment_name + '_' + model_name + "_pr_recall_curve.png")


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

    # print_scatter_matrix(stats_location,
    #                      df,
    #                      title='\n' + experiment_name + '\n\n' + "Scatter Matrix",
    #                      file_name=prefix + "scatter_m3x.png",
    #                      export=export)
