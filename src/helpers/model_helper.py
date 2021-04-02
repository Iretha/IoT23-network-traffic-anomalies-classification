import logging
import os
import pickle
import sys
import time

from src.helpers.log_helper import log_duration
from src.helpers.dataframe_helper import load_data


def create_models(models_dir,
                  train_data_file_path,
                  features,
                  classification_col,
                  algorithms,
                  overwrite=False):
    logging.info("-----> Train " + str(len(algorithms)) + " models : " + str(algorithms))
    start_time = time.time()

    # Load Data
    x_train, y_train = load_data(train_data_file_path, classification_col, features=features)

    # Train & Save Models
    for model_name in algorithms.keys():
        model_path = models_dir + model_name + '.pkl'
        exists = os.path.exists(model_path)

        if not exists or overwrite:
            trained_model = None

            # Train
            try:
                trained_model = train_model(model_name, algorithms[model_name], x_train, y_train)
            except:
                logging.error("Oops! Could not train with model " + model_name + " data=" + train_data_file_path, sys.exc_info()[0], " occurred.")

            # Save
            if trained_model is not None:
                try:
                    save_model(model_path, trained_model)
                except:
                    logging.error("Oops! Could not save model " + model_name + " in " + models_dir + '; ' + train_data_file_path, sys.exc_info()[0], " occurred.")
        else:
            logging.warning('^^^^^ Model ' + model_name + ' already exists! Skip training...')

    log_duration(start_time, '-----> Training of all models finished in')


def train_model(model_name, model, x_train, y_train):
    logging.info("=====> Train " + model_name + " . . .")
    start_time = time.time()

    model.fit(x_train, y_train)

    log_duration(start_time, "=====> Training of " + model_name + " finished in")
    return model


def save_model(model_path, model):
    # Save Model
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)


def load_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        logging.info('Model loaded: ' + model_path)
        return model
    return None
