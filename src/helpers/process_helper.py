from src.helpers.data_helper import run_data_preprocessing
from src.helpers.data_stats_helper import explore_clean_data, explore_experiments_train_test_data
from src.helpers.experiments_helper import run_experiments
from src.helpers.file_helper import list_folder_names
from src.helpers.model_stats_helper import run_experiments_reports
from src.helpers.report_helper import combine_reports
from src.iot23 import iot23_metadata, data_cleanup


def run_end_to_end_process(source_files_dir,
                           data_dir,
                           experiments_dir,
                           data_samples,
                           features,
                           training_algorithms,
                           report_file_name):
    file_header = iot23_metadata["file_header"]

    # Prepare Data
    run_data_preprocessing(source_files_dir,
                           data_dir,
                           file_header,
                           data_cleanup,
                           data_samples=data_samples,
                           overwrite=False)

    # Explore Data
    explore_clean_data(data_dir,
                       data_samples=data_samples,
                       plot_corr=True,
                       plot_cls_dist=True,
                       plot_attr_dist=True)

    # Run Experiments
    run_experiments(data_dir,
                    experiments_dir,
                    data_samples,
                    features,
                    training_algorithms,
                    overwrite=False)

    # Explore Train/ Test Data
    explore_experiments_train_test_data(experiments_dir,
                                        data_samples,
                                        features,
                                        plot_corr=True,
                                        plot_cls_dist=True,
                                        plot_attr_dist=True)

    # Explore Experiments Output
    run_experiments_reports(experiments_dir,
                            data_samples,
                            features,
                            enable_score_tables=True,
                            enable_score_charts=True,
                            enable_model_insights=True)

    # Combine all stats into single XLS
    experiments_folder_list = list_folder_names(experiments_dir)
    combine_reports(experiments_dir, experiments_folder_list, report_file_name)
