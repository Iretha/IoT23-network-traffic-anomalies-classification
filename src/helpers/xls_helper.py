import logging
import time
import xlsxwriter

from src.iot23 import get_feat_selection_name, get_data_sample_name, get_sample_row_count, get_data_sample_name_short
from src.iot23 import decode_cls_label


def export_stats_xls(output_dir,
                     exp_stats_dict,
                     output_file_name='stats.xlsx'):
    file_path = output_dir + output_file_name

    logging.info("===== Export xlsx file: " + file_path)
    start_time = time.time()

    workbook = xlsxwriter.Workbook(file_path)
    try:
        __create_overall_scores_worksheet(workbook, exp_stats_dict, title="Model Overall Scores")
        __create_class_scores_worksheet(workbook, exp_stats_dict, title="Model Class Scores")
        __create_aggr_features_scores_worksheet(workbook, exp_stats_dict, title="Aggregated Scores")
    finally:
        if workbook is not None:
            workbook.close()

    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info("===== Xlsx file in %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))


def __create_overall_scores_worksheet(workbook, exp_stats_dict, title="Model Scores"):
    header = [
        'Features',
        'Data',
        'Rows',
        'Algorithm',
        'Accuracy',
        'Balanced Accuracy',
        'Precision (Weighted)',
        'Precision (Macro)',
        'Precision (Micro)',
        'Recall (Weighted)',
        'Recall (Macro)',
        'Recall (Micro)',
        'F1-Score (Weighted)',
        'F1-Score (Macro)',
        'F1-Score (Micro)',
        'Support (Weighted)',
        'Support (Macro)',
        'Runtime (sec)',
        'CPU (%)',
        'Process Memory (%)',
    ]
    content = [header]
    exp_stat_names = exp_stats_dict.keys()
    for exp_stat_name in exp_stat_names:
        exp_stats = exp_stats_dict[exp_stat_name]
        __create_overall_model_scores_content(content, exp_stat_name, exp_stats)

    worksheet = workbook.add_worksheet(name=title)
    __write_sheet_content(worksheet, content)


def __create_overall_model_scores_content(content, exp_name, exp_stats):
    model_stats = exp_stats['model_stats']
    model_names = model_stats.keys()
    for model_name in model_names:
        if model_stats[model_name] is None:
            logging.warning("No stats json for exp=" + exp_name + " and model=" + model_name)
            continue
        row_content = [get_feat_selection_name(exp_name),
                       get_data_sample_name_short(exp_name),
                       get_sample_row_count(exp_name),
                       model_name]
        row_content.extend(__gen_metric_cells(model_stats[model_name]))
        content.append(row_content)
    return content


def __gen_metric_cells(stats):
    model_cls_report = stats['classification_report']
    adv_stats = stats['adv_stats']
    metric_cells = [model_cls_report["accuracy"],
                    stats['balanced_accuracy'],
                    model_cls_report["weighted avg"]["precision"],
                    model_cls_report["macro avg"]["precision"],
                    stats["precision_score_micro"],
                    model_cls_report["weighted avg"]["recall"],
                    model_cls_report["macro avg"]["recall"],
                    stats["recall_score_micro"],
                    model_cls_report["weighted avg"]["f1-score"],
                    model_cls_report["macro avg"]["f1-score"],
                    stats['f1_score_micro'],
                    model_cls_report["weighted avg"]["support"],
                    model_cls_report["macro avg"]["support"],
                    adv_stats['Runtime (sec)'],
                    adv_stats['CPU'],
                    adv_stats['Process Memory']]
    return metric_cells


def __create_class_scores_worksheet(workbook, exp_stats_dict, title="Class Scores"):
    header = [
        'Features',
        'Data',
        'Rows',
        'Algorithm',
        'Class',
        'Class Code',
        'Precision',
        'Recall',
        'F1-Score',
        'Support',
    ]
    content = [header]
    exp_stat_names = exp_stats_dict.keys()
    for exp_stat_name in exp_stat_names:
        exp_stats = exp_stats_dict[exp_stat_name]
        __create_class_model_scores_content(content, exp_stat_name, exp_stats)

    worksheet = workbook.add_worksheet(name=title)
    __write_sheet_content(worksheet, content)


def __create_class_model_scores_content(content, exp_name, exp_stats):
    model_stats = exp_stats['model_stats']
    model_names = model_stats.keys()
    for model_name in model_names:
        if model_stats[model_name] is None:
            logging.warning("No stats json for exp=" + exp_name + " and model=" + model_name)
            continue

        model_cls_report = model_stats[model_name]['classification_report']
        keys = model_cls_report.keys()
        filtered_keys = [x for x in keys if x.isnumeric()]
        for key in filtered_keys:
            key_num = int(key)
            label = decode_cls_label(key_num)
            row_cells = [get_feat_selection_name(exp_name),
                         get_data_sample_name_short(exp_name),
                         get_sample_row_count(exp_name),
                         model_name,
                         label,
                         key_num,
                         model_cls_report[key]["precision"],
                         model_cls_report[key]["recall"],
                         model_cls_report[key]["f1-score"],
                         model_cls_report[key]["support"]]
            content.append(row_cells)
    return content


def __create_aggr_features_scores_worksheet(workbook, exp_stats_dict, title="Agg Scores"):
    column_labels = [
        ['', ''],
        ['', ''],
        ['', ''],
        ['Accuracy', ''],
        ['Accuracy', 'Balanced'],
        ['Precision', 'Weighted'],
        ['Precision', 'Macro'],
        ['Precision', 'Micro'],
        ['Recall', 'Weighted'],
        ['Recall', 'Macro'],
        ['Recall', 'Micro'],
        ['F1 Score', 'Weighted'],
        ['F1 Score', 'Macro'],
        ['F1 Score', 'Micro'],
        ['Support', 'Weighted'],
        ['Support', 'Macro'],
        ['Runtime', 'sec'],
        ['CPU', '%'],
        ['Memory', '%'],
    ]
    aggregated_data = __aggregate_by_features(exp_stats_dict)

    empty_rows = [[], []]
    rows = []
    rows.extend(empty_rows)
    for key in aggregated_data:
        table_content_cols = __create_aggr_features_table(key, aggregated_data[key])
        table_rows = __create_excel_rows_from_cols(column_labels, table_content_cols)
        rows.extend(table_rows)
        rows.extend(empty_rows)

    worksheet = workbook.add_worksheet(name=title)
    __write_sheet_content(worksheet, rows)


def __create_aggr_features_table(feature_def_name, table_data):
    model_names = sorted(table_data.keys())

    columns = []
    for model_name in model_names:
        data_sets = table_data[model_name].keys()
        for data_set in data_sets:
            col = [feature_def_name, model_name, data_set]
            col.extend(__gen_metric_cells(table_data[model_name][data_set]))
            columns.append(col)
    return columns


def __create_excel_rows_from_cols(header_cols, content_cols):
    rows = []
    for col_idx in range(len(content_cols)):
        if col_idx == 0:  # Add left headers
            for header_idx in range(len(header_cols)):
                row = []
                for h_cell in header_cols[header_idx]:
                    row.append(h_cell)
                rows.append(row)

        column = content_cols[col_idx]
        for row_idx in range(len(column)):
            rows[row_idx].append(column[row_idx])
    return rows


def __aggregate_by_features(exp_stats_dict):
    exp_names = exp_stats_dict.keys()
    grouped_by_feat_data = {}
    for exp_name in exp_names:
        feat_def = get_feat_selection_name(exp_name)
        data_def = get_data_sample_name(exp_name)
        if feat_def not in grouped_by_feat_data:
            grouped_by_feat_data[feat_def] = {}
        if data_def not in grouped_by_feat_data[feat_def]:
            grouped_by_feat_data[feat_def][data_def] = exp_stats_dict[exp_name]['model_stats']

    groups = {}
    for feat in sorted(grouped_by_feat_data.keys()):
        for data in sorted(grouped_by_feat_data[feat].keys()):
            model_names = grouped_by_feat_data[feat][data].keys()
            for model_name in model_names:
                if feat not in groups:
                    groups[feat] = {}

                if model_name not in groups[feat]:
                    groups[feat][model_name] = {}

                if data not in groups[feat][model_name]:
                    groups[feat][model_name][data] = grouped_by_feat_data[feat][data][model_name]
    return groups


def __write_sheet_content(worksheet, content):
    row = 0
    for line in content:
        column = 0
        for cell in line:
            worksheet.write(row, column, cell)
            column += 1
        row += 1
