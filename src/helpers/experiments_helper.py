import logging

from src.iot23 import get_exp_name, get_exp_data_dir, get_exp_models_dir, data_cleanup, get_train_data_path
from src.helpers.file_helper import mk_dir
from src.helpers.data_helper import split_into_train_and_test
from src.helpers.model_helper import create_models


def train_models(data_dir,
                 experiments_dir,
                 data_samples,
                 features_selections,
                 training_algorithms,
                 overwrite=False,
                 enable_model_training=True):
    for data_sample in data_samples:
        for feature_selection in features_selections:
            __train_models(data_dir,
                           experiments_dir,
                           data_sample,
                           feature_selection,
                           training_algorithms,
                           overwrite=overwrite,
                           enable_model_training=enable_model_training)


def __train_models(data_dir,
                   experiments_dir,
                   data_sample,
                   feature_selection,
                   training_algorithms,
                   overwrite=False,
                   enable_model_training=True):
    experiment_name = get_exp_name(data_sample, feature_selection['description'])
    data_file_name = data_sample['clean_data_file_name']
    features = feature_selection['features']

    # Make experiment models dir
    experiment_models_dir = experiments_dir + get_exp_models_dir(experiment_name)
    mk_dir(experiment_models_dir)

    # Train models
    if enable_model_training:
        classification_col = data_cleanup["classification_col"]
        train_data_file_path = data_dir + get_train_data_path(data_file_name)
        create_models(experiment_models_dir,
                      train_data_file_path,
                      features,
                      classification_col,
                      training_algorithms,
                      overwrite=overwrite)
        logging.info("****** Experiment models are in " + experiment_models_dir)
