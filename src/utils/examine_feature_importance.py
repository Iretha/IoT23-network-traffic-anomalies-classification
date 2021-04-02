import logging

from sklearn.inspection import permutation_importance

from src.helpers.dataframe_helper import load_data
from src.helpers.model_helper import load_model
from src.helpers.plt_helper import plot_feature_importance, plot_permutation_importance
from src.iot23 import data_cleanup


def examine_feat_perm_imp(dest_dir,
                       experiment_name,
                       model_name,
                       model,
                       mode='f',
                       test_data_file_path=None):
    if mode == 'f':
        feature_importance = None
        try:
            feature_importance = model.feature_importances_
        except:
            try:
                feature_importance = model.coef_[0]
            except:
                logging.error("Oops! Feat Importance could not be extracted for " + model_name)

        if feature_importance is not None:
            print(feature_importance)
            plot_feature_importance(dest_dir,
                                    model_name,
                                    experiment_name,
                                    feature_importance,
                                    title=experiment_name + "\n\n" + model_name + "\nFeature Importance",
                                    file_name=model_name + "_feature_imp.png")

    else:
        try:
            classification_col = data_cleanup["classification_col"]
            x_test, y_test = load_data(test_data_file_path, classification_col)
            permut_importance = permutation_importance(model, x_test, y_test)

            if permut_importance is not None:
                print(permut_importance)
                plot_permutation_importance(dest_dir,
                                            model_name,
                                            experiment_name,
                                            permut_importance,
                                            title=experiment_name + "\n\n" + model_name + "\nPermutation Importance",
                                            file_name=model_name + "_permutation_imp.png")
        except:
            logging.error("Oops! Permutation Importance could not be extracted for " + model_name)



output_dir = 'E:\\machine-learning\\datasets\\iot23\\tmp\\'
experiments_dir = 'E:\\machine-learning\\datasets\\iot23\\4_experiments\\'
test_data_file_path_f19_s04= experiments_dir + "F19_S04_R_5_000_000\data\S04_R_5_000_000_clean.csv_test.csv"
model_nb_f19_s04_path = experiments_dir + "F19_S04_R_5_000_000\models\GaussianNB.pkl"
model_nb_f19_s04 = load_model(model_nb_f19_s04_path)
examine_feat_perm_imp(output_dir, 'F19_S04', 'NB_F19_S04', model_nb_f19_s04, mode='p', test_data_file_path=test_data_file_path_f19_s04)

test_data_file_path_f18_s16= experiments_dir + "F18_S16_R_5_000_000\data\S16_R_5_000_000_clean.csv_test.csv"
model_nb_f18_s16_path = experiments_dir + "F18_S16_R_5_000_000\models\GaussianNB.pkl"
model_nb_f18_s16 = load_model(model_nb_f18_s16_path)
examine_feat_perm_imp(output_dir, 'F18_S16', 'NB_F18_S16', model_nb_f18_s16, mode='p', test_data_file_path=test_data_file_path_f18_s16)

print('The end')
quit()