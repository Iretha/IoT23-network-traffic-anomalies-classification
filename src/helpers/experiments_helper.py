import logging

from src.iot23 import get_exp_name, get_exp_data_dir, get_exp_models_dir, data_cleanup, get_train_data_path
from src.helpers.file_helper import mk_dir
from src.helpers.data_helper import split_into_train_and_test
from src.helpers.model_helper import create_models


def run_model_training_for_samples(data_dir,
                                   experiments_dir,
                                   data_samples,
                                   features_selections,
                                   training_algorithms,
                                   test_size=0.2,
                                   overwrite=False):
    for data_sample in data_samples:
        for feature_selection in features_selections:
            run_model_training_for_sample(data_dir,
                                          experiments_dir,
                                          data_sample,
                                          feature_selection,
                                          training_algorithms,
                                          test_size=test_size,
                                          overwrite=overwrite)


def run_model_training_for_sample(data_dir,
                                  experiments_dir,
                                  data_sample,
                                  feature_combination,
                                  training_algorithms,
                                  test_size=0.2,
                                  overwrite=False):
    # Make experiment data dir
    experiment_name = get_exp_name(data_sample, feature_combination)
    experiment_data_dir = experiments_dir + get_exp_data_dir(experiment_name)
    mk_dir(experiment_data_dir)

    # Prepare experiment data
    data_file_name = data_sample['clean_data_file_name']
    split_into_train_and_test(data_dir,
                              data_file_name,
                              experiment_data_dir,
                              test_size=test_size,
                              features=feature_combination['features'],
                              overwrite=overwrite)
    logging.info("****** Experiment data is in " + experiment_data_dir)

    # Make experiment models dir
    experiment_models_dir = experiments_dir + get_exp_models_dir(experiment_name)
    mk_dir(experiment_models_dir)

    # Train models
    classification_col = data_cleanup["classification_col"]
    train_data_file_path = experiment_data_dir + get_train_data_path(data_file_name)
    create_models(experiment_models_dir,
                  train_data_file_path,
                  classification_col,
                  training_algorithms,
                  overwrite=overwrite)
    logging.info("****** Experiment models are in " + experiment_models_dir)
