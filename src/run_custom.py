import warnings

import sklearn
from numpy import sort
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from config import iot23_attacks_dir, iot23_data_dir, iot23_experiments_dir
from src.helpers.data_helper import prepare_data
from src.helpers.data_stats_helper import explore_data
from src.helpers.experiments_helper import train_models
from src.helpers.file_helper import list_folder_names
from src.helpers.log_helper import add_logger
from src.helpers.model_stats_helper import export_model_stats
from src.helpers.report_helper import combine_reports
from src.iot23 import get_data_sample, iot23_metadata, feature_selections, data_cleanup

# Add Logger
add_logger(file_name='custom.log')

# Setup warnings
warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=sklearn.exceptions.ConvergenceWarning)

file_header = iot23_metadata["file_header"]
source_files_dir = iot23_attacks_dir
data_dir = iot23_data_dir
experiments_dir = iot23_experiments_dir
data_samples = [
    get_data_sample(dataset_name='S04', rows_per_dataset_file=10_000),
    get_data_sample(dataset_name='S16', rows_per_dataset_file=10_000),
]

# Selected Features
features = [
    feature_selections['F14'],
    # feature_selections['F17'],
    # feature_selections['F18'],
    # feature_selections['F19'],
]

# Selected Algorithms
training_algorithms = dict([
    ('DecisionTree', Pipeline([('normalization', StandardScaler()), ('classifier', DecisionTreeClassifier())])),
    ('GaussianNB', Pipeline([('normalization', StandardScaler()), ('classifier', GaussianNB())])),
    ('LogisticRegression', Pipeline([('normalization', StandardScaler()), ('classifier', LogisticRegression())])),
    ('RandomForest', Pipeline([('normalization', StandardScaler()), ('classifier', RandomForestClassifier())])),
    ('SVC_linear', Pipeline([('normalization', MinMaxScaler()), ('classifier', LinearSVC())])),
])

# Prerequisites:
# 1. Run run_step00_configuration_check.py
# 2. Run run_step01_extract_data_from_scenarios.py
# 3. Run run_step01_shuffle_file_content.py

# Run Data Preprocessing
prepare_data(source_files_dir,
             data_dir,
             iot23_metadata["file_header"],
             data_cleanup,
             test_size=0.2,
             data_samples=data_samples,
             overwrite=True)

# Export Data Charts & Stats
explore_data(data_dir,
             data_samples=data_samples,
             explore_data_sample=True,
             explore_split_data=True,
             plot_corr=True,
             plot_cls_dist=True,
             plot_attr_dist=True)

# Train models
train_models(data_dir,
             experiments_dir,
             data_samples,
             features,
             training_algorithms,
             overwrite=False)

# Export Model Stats & Charts
export_model_stats(data_dir,
                   experiments_dir,
                   data_samples,
                   features,
                   enable_score_tables=True,
                   enable_score_charts=True,
                   enable_model_insights=False)

# Combine all reports
exp_dir = iot23_experiments_dir
exp_list_all = sort(list_folder_names(exp_dir))
combine_reports(exp_dir, exp_list_all, 'S04_S16_all_scores.xlsx')

print('Custom: The end.')
quit()
