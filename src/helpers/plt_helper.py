import logging
import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scikitplot as sk_plt
from pandas.plotting import scatter_matrix
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels

from src.iot23 import get_feature_selection, decode_labels


def plot_correlations(output_dir,
                      corr,
                      title="Correlations",
                      file_name="correlations.png",
                      abs_mode=True,
                      export=True):
    columns_count = len(corr.columns)
    file_path = output_dir + file_name

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=[columns_count, columns_count])
    fig.suptitle(title, fontsize=20)

    if abs_mode:
        corr = corr.abs()

    ax = sns.heatmap(corr, annot=True, fmt='.0%', cmap='Greens', ax=ax)
    export_sns(fig, file_path, export=export)


def plot_class_values_distribution(output_dir,
                                   df,
                                   col_name,
                                   title="Class Frequency",
                                   file_name="data_distribution.png",
                                   export=True):
    unique, counts = np.unique(df[col_name], return_counts=True)
    values = counts
    x_values = unique

    file_path = output_dir + file_name
    x = decode_labels(x_values)
    x_pos = [i for i, _ in enumerate(x)]
    size = len(x)
    cnt = size + 2 if size < 5 else size * 0.5

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(cnt, cnt))
    fig.subplots_adjust(bottom=0.15, left=0.15, top=0.8)
    fig.suptitle(title, fontsize=18)
    ax.bar(x_pos, values, color='orange', alpha=0.6)
    # ax.set_title(title)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Class')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(
        x,
        rotation=35,
        ha="right",
        rotation_mode="anchor")

    # plt.xticks(x_pos, x)

    export_plt(file_path)


def plot_attr_values_distribution(output_dir,
                                  df,
                                  title='Attribute Distribution',
                                  file_name='attr_distribution.png',
                                  export=True):
    file_path = output_dir + file_name
    columns_count = len(df.columns)

    plt.style.use('ggplot')
    df.hist(alpha=0.6, figsize=(columns_count + 1, columns_count + 1), color='green')
    plt.suptitle(title, fontsize=18)
    export_plt(file_path)


def plot_confusion_ma3x(output_dir,
                        y_test,
                        predictions,
                        title="Confusion Matrix",
                        file_name="conf_ma3x.png"):
    classes = unique_labels(y_test, predictions)
    cnt = len(classes)
    cnt = cnt * 2 if cnt < 10 else cnt * 0.7
    # labels = decode_labels(classes)

    sk_plt.metrics.plot_confusion_matrix(y_test,
                                         predictions,
                                         normalize=True,
                                         title=title + " (Normalized)",
                                         title_fontsize="large",
                                         figsize=(cnt, cnt))
    export_plt(output_dir + file_name + '_n.png')


def plot_confusion_ma3x_v2(output_dir,
                           y_test,
                           predictions,
                           title="Confusion Matrix",
                           file_name="conf_ma3x_v2.png",
                           export=True):
    classes = unique_labels(y_test, predictions)
    cnt = len(classes)
    small = cnt < 10
    left = 0.2 if small else 0.12
    size = cnt * 1.5 if small else cnt * 0.8
    labels = decode_labels(classes)

    fig, ax = plt.subplots(1, 1, figsize=(size, size))
    fig.subplots_adjust(left=left)
    ax = sk_plt.metrics.plot_confusion_matrix(y_test,
                                              predictions,
                                              normalize=True,
                                              title=title + " (Normalized)",
                                              title_fontsize="large",
                                              ax=ax)
    ax.set_xticklabels(labels, rotation=35)
    ax.set_yticklabels(labels)
    export_plt(output_dir + file_name)


def plot_model_roc_curve(output_dir,
                         model,
                         model_name,
                         x_test,
                         y_true,
                         experiment_name,
                         title="ROC Curve",
                         file_name="roc_curve.png"):
    try:
        y_prob = model.predict_proba(x_test)
        plot_roc_custom(output_dir, y_true, y_prob, experiment_name, model_name, file_name, "ROC")
    except:
        try:
            y_decision_auc = model.decision_function(x_test)
            plot_roc_custom(output_dir, y_true, y_decision_auc, experiment_name, model_name, file_name, "AUC")
        except:
            logging.error("!!! Run test data fix to plot ROC for " + model_name, sys.exc_info()[0])


def plot_roc_custom(output_dir, y_true, y_prob, name, model_name, file_name, type):
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(top=0.8, right=0.65)
        sk_plt.metrics.plot_roc(y_true,
                                y_prob,
                                title=name + "\n\n" + model_name + "\n" + type + " Curve\n",
                                cmap='nipy_spectral',
                                ax=ax,
                                plot_micro=False,
                                plot_macro=False)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='best', fontsize='medium')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='best', fontsize='medium')
        export_plt(output_dir + file_name + '_' + type + '.png')
    except:
        logging.error("Oops! Could not plot " + type + " Curve for model " + name)


def plot_model_precision_recall_curve(output_dir,
                                      model,
                                      model_name,
                                      x_test,
                                      y_true,
                                      experiment_name,
                                      title="Precision Recall Curve",
                                      file_name="pr_recall_curve.png"):
    try:
        y_prob = model.predict_proba(x_test)
        plot_precision_recall_curve_custom(output_dir, y_true, y_prob, experiment_name, model_name, file_name, "Precision-Recall")
    except:
        try:
            y_decision_auc = model.decision_function(x_test)
            plot_precision_recall_curve_custom(output_dir, y_true, y_decision_auc, experiment_name, model_name, file_name, "Precision-Recall_AUC")
        except:
            logging.error("Run test data fix to plot ROC for " + model_name)


def plot_precision_recall_curve_custom(output_dir, y_true, y_prob, name, model_name, file_name, type):
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(top=0.8, right=0.55)
        sk_plt.metrics.plot_precision_recall(y_true, y_prob, title=name + "\n\n" + model_name + "\n" + type + " Curve\n", cmap='nipy_spectral', ax=ax, plot_micro=False)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='best', fontsize='medium')
        export_plt(output_dir + file_name + '_' + type + '.png')
    except:
        logging.error("Oops! Could not export Precision/ Recall Curve for model " + model_name)


def plot_feature_importance(results_location,
                            model_name,
                            experiment_name,
                            feat_importance,
                            title="Feature Importance",
                            file_name="feat_imp.png"):
    feature_names = get_feature_selection(experiment_name)

    values = list(feat_importance.values())
    x_pos = [x for x in range(len(values))]

    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25, top=0.75, left=0.15)
    ax.bar(x_pos, values, color='orange', alpha=0.6)
    ax.set_title(title)
    ax.set_ylabel('Importance')
    ax.set_xlabel('Features')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(
        feature_names[0:len(values)],
        rotation=35,
        ha="right",
        rotation_mode="anchor")
    export_plt(results_location + file_name)


def export_plt(file_path, export=True):
    if export:
        plt.savefig(file_path)
        plt.close()
        plt.cla()
    else:
        plt.show()


def export_sns(fig, file_path, export=True):
    if export:
        fig.savefig(file_path)
        plt.close()
        plt.cla()
    else:
        plt.show()


def plot_permutation_importance(results_location,
                                model_name,
                                experiment_name,
                                permutation_importance,
                                title="Permutation Importance",
                                file_name="permut_imp.png"):
    columns = permutation_importance['columns']
    sorted_idx = permutation_importance.importances_mean.argsort()

    fig, ax = plt.subplots()
    ax.boxplot(permutation_importance.importances[sorted_idx].T, labels=columns[sorted_idx], vert=False)
    ax.set_title("Permutation Importances")
    fig.tight_layout()
    export_plt(results_location + file_name)
    export_plt(results_location + file_name)


def print_scatter_matrix(output_dir,
                         df,
                         title='Scatter MAtrix',
                         file_name="feature_distribution.png",
                         export=True):
    file_path = output_dir + file_name
    cnt = len(df.columns)

    plt.style.use('ggplot')
    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(cnt * 2, cnt * 2), color='black')
    export_plt(file_path, export=export)
