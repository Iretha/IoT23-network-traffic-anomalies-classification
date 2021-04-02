from helpers.dataframe_helper import df_get


def examine_file_content(file_path):
    print('A')
    df = df_get(file_path, delimiter=',')
    # df['detailed-label'].value_counts()
    df_counts = df['detailed-label'].value_counts()
    print(df_counts)


output_dir = 'E:\\machine-learning\\datasets\\iot23\\tmp\\'
experiments_dir = 'E:\\machine-learning\\datasets\\iot23\\4_experiments\\'
data_file_path = experiments_dir + 'F14_S16_R_5_000_000\data\S16_R_5_000_000_clean.csv_test.csv'
examine_file_content(data_file_path)
