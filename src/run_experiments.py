import warnings

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from config import iot23_attacks_dir, iot23_data_dir, iot23_experiments_dir
from src.helpers.log_helper import add_logger
from src.helpers.process_helper import run_end_to_end_process
from src.iot23 import get_data_sample, iot23_metadata, feature_selections

# Add Logger
add_logger(file_name='experiments.log')

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

file_header = iot23_metadata["file_header"]
source_files_dir = iot23_attacks_dir
data_dir = iot23_data_dir
experiments_dir = iot23_experiments_dir
data_samples = [
    get_data_sample(dataset_name='S04', rows_per_dataset_file=5_000_000),
    get_data_sample(dataset_name='S16', rows_per_dataset_file=5_000_000),
]

# Selected Features
features = [
    feature_selections['F14'],
    feature_selections['F17'],
    feature_selections['F18'],
    feature_selections['F19'],
]

# Selected Algorithms
training_algorithms = dict([
    ('DecisionTree', Pipeline([('normalization', StandardScaler()), ('classifier', DecisionTreeClassifier())])),
    ('GaussianNB', Pipeline([('normalization', StandardScaler()), ('classifier', GaussianNB())])),
    ('LogisticRegression', Pipeline([('normalization', StandardScaler()), ('classifier', LogisticRegression())])),
    ('RandomForest', Pipeline([('normalization', StandardScaler()), ('classifier', RandomForestClassifier())])),
    ('SVC_linear', Pipeline([('normalization', MinMaxScaler()), ('classifier', LinearSVC())])),
])

run_end_to_end_process(source_files_dir,
                       data_dir,
                       experiments_dir,
                       data_samples,
                       features,
                       training_algorithms,
                       final_report_name='experiment_scores.xlsx')
