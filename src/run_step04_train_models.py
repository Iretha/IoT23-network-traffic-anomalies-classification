from config import iot23_data_dir, iot23_experiments_dir
from src.iot23 import data_samples, feature_selections
from src.helpers.log_helper import add_logger
from src.helpers.experiments_helper import run_combinations

add_logger(file_name='04_train_models.log')

# Selected Data Files
data_file_dir = iot23_data_dir
data_combinations = [
    # data_combinations['S13_R_100_000'],  # 10 sec
    # data_combinations['S13_R_5_000_000'],  # 30 sec
    data_samples['S04_R_5_000_000'],  # 30 sec
    data_samples['S16_R_5_000_000'],  # 30 sec
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

    # ('DecisionTree', Pipeline([('normalization', MinMaxScaler()), ('classifier', DecisionTreeClassifier())])),  # 5 mil = 2 min
    # ('GaussianNB', Pipeline([('normalization', StandardScaler()), ('classifier', GaussianNB())])),  # 5 mil = 11 sec
    # ('GaussianNB_mm', Pipeline([('normalization', MinMaxScaler()), ('classifier', GaussianNB())])),  # 5 mil = 11 sec
    # ('LogisticRegression', Pipeline([('normalization', StandardScaler()), ('classifier', LogisticRegression())])),  # 5 mil = 20 min
    # ('LogisticRegression_mm', Pipeline([('normalization', MinMaxScaler()), ('classifier', LogisticRegression())])),
    # ('RandomForest', Pipeline([('normalization', StandardScaler()), ('classifier', RandomForestClassifier())])),  # 5 mil = 60 min
    # ('RandomForest_mm', Pipeline([('normalization', StandardScaler()), ('classifier', RandomForestClassifier())])),  # 5 mil = 60 min
    # ('SVC_linear', Pipeline([('normalization', MinMaxScaler()), ('classifier', LinearSVC())])),  # 5 mil = 60 min

    # ('AdaBoost', Pipeline([('normalization', MinMaxScaler()), ('classifier', AdaBoostClassifier(n_estimators=1000))])),  # 5 mil = 2 min
    # ('MLPClassifier', Pipeline([('normalization', MinMaxScaler()), ('classifier', MLPClassifier(hidden_layer_sizes=(15,), max_iter=1000))])),  # 8.313 min
    # ('AdaBoost_Decision_Tree', Pipeline([('normalization', StandardScaler()), ('classifier', AdaBoostClassifier(DecisionTreeClassifier(max_depth=2), n_estimators=1000))])),
    # ('GradientBoostingClassifier', Pipeline([('normalization', StandardScaler()), ('classifier', GradientBoostingClassifier())])),  # 5 mil = 60 min
])

experiments_dir = iot23_experiments_dir
run_combinations(data_file_dir,
                 experiments_dir,
                 data_combinations,
                 features,
                 training_algorithms,
                 overwrite=False)

print('Step 04: The end.')
quit()
