import logging
import time

from src.iot23 import data_cleanup, get_exp_name, get_exp_data_dir, get_train_data_path, get_test_data_path
from src.helpers.dataframe_helper import df_get
from src.helpers.log_helper import log_duration
from src.helpers.plt_helper import plot_correlations, plot_class_values_distribution, plot_attr_values_distribution


def explore_data(data_dir,
                 data_samples=None,
                 explore_data_sample=True,
                 explore_split_data=False,
                 plot_corr=False,
                 plot_cls_dist=False,
                 plot_attr_dist=False):
    if data_samples is None:
        return

    logging.info("-----> Explore data for  . . . " + str(data_samples))
    start_time = time.time()

    for data_sample in data_samples:
        data_file_name = data_sample['clean_data_file_name']
        data_file_path = data_dir + data_file_name
        data_info = data_sample['description']

        if explore_data_sample:
            # Explore Sample Data
            __explore_data(data_file_path,
                           data_dir,
                           data_info,
                           data_file_name,
                           plot_corr=plot_corr,
                           plot_cls_dist=plot_cls_dist,
                           plot_attr_dist=plot_attr_dist)

        if explore_split_data:
            # Explore Train Data
            train_data_file_name = get_train_data_path(data_sample['clean_data_file_name'])
            __explore_data(data_dir + train_data_file_name,
                           data_dir,
                           data_info + ' Train',
                           data_info + '_train_',
                           plot_corr=plot_corr,
                           plot_cls_dist=plot_cls_dist,
                           plot_attr_dist=plot_attr_dist)

            # Explore Test Data
            test_data_file_name = get_test_data_path(data_sample['clean_data_file_name'])
            __explore_data(data_dir + test_data_file_name,
                           data_dir,
                           data_info + ' Test',
                           data_info + '_test_',
                           plot_corr=plot_corr,
                           plot_cls_dist=plot_cls_dist,
                           plot_attr_dist=plot_attr_dist)

    log_duration(start_time, '-----> Exploration finished in')


def __explore_data(data_file_path,
                   data_dir,
                   info,
                   output_file_name_prefix,
                   plot_corr=False,
                   plot_cls_dist=False,
                   plot_attr_dist=False):
    logging.info("-----> -----> Explore data for  . . . " + data_file_path)
    start_time = time.time()

    # Load data in df
    df = df_get(data_file_path, delimiter=',')

    # Data Correlations
    if plot_corr:
        plot_correlations(data_dir,
                          df.corr(),
                          title='\n' + info + '\n\n' + "Correlations",
                          file_name=output_file_name_prefix + "_correlations.png",
                          abs_mode=True,
                          export=True)

    # Data distribution per class
    if plot_cls_dist:
        plot_class_values_distribution(data_dir,
                                       df,
                                       data_cleanup['classification_col'],
                                       title='\n' + info + '\n\n' + "Class Frequency",
                                       file_name=output_file_name_prefix + "_class_values_distribution.png",
                                       export=True)
    # Data distribution per attribute
    if plot_attr_dist:
        plot_attr_values_distribution(data_dir,
                                      df,
                                      title='\n' + info + '\n\n' + "Value Distribution",
                                      file_name=output_file_name_prefix + "_attr_values_distribution.png",
                                      export=True)
    log_duration(start_time, '-----> -----> Exploration finished in')
