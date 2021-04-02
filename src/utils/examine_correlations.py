from src.helpers.dataframe_helper import df_get
from src.helpers.plt_helper import plot_correlations
from src.iot23 import feature_selections


def examine_corr(data_file_path, title, feature_comb=None):
    df = df_get(data_file_path, delimiter=',')
    features = []
    if feature_comb is not None:
        features = feature_selections[feature_comb]

    corr = df.corr() if len(features) == 0 else df[features].corr()

    plot_correlations(output_dir,
                      corr,
                      title=title,
                      file_name=title + '.png')


output_dir = 'E:\\machine-learning\\datasets\\iot23\\tmp\\'
experiments_dir = 'E:\\machine-learning\\datasets\\iot23\\4_experiments\\'
data_file_path_f19_s04 = experiments_dir + 'F19_S04_R_5_000_000\data\S04_R_5_000_000_clean.csv_train.csv'
examine_corr(data_file_path_f19_s04, title="F19_S04_Train")

data_file_path_f18_s16 = experiments_dir + 'F18_S16_R_5_000_000\data\S16_R_5_000_000_clean.csv_train.csv'
examine_corr(data_file_path_f18_s16, title="F18_S16_Train")

print('The end.')
quit()
