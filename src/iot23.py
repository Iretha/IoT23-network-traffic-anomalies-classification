import re

iot23_metadata = {
    "file_name_pattern": "/**/conn.log.labeled",
    "file_header": "ts	uid	id.orig_h	id.orig_p	id.resp_h	id.resp_p	"
                   "proto	service	duration	orig_bytes	resp_bytes	conn_state	"
                   "local_orig	local_resp	missed_bytes	history	orig_pkts	"
                   "orig_ip_bytes	resp_pkts	resp_ip_bytes	tunnel_parents	"
                   "label	detailed-label\n",
    "all_columns": [
        'ts', 'uid',
        'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
        'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
        'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
        'label', 'detailed-label'
    ],
    "numeric_columns": ["duration",
                        "orig_bytes",
                        "resp_bytes",
                        "missed_bytes",
                        "local_orig",
                        "local_resp",
                        "orig_pkts",
                        "orig_ip_bytes",
                        "resp_pkts",
                        "resp_ip_bytes"],
}

data_cleanup = {
    "classification_col": "detailed-label",
    "drop_cols": ['ts', 'uid', 'label'],
    "replace_values": {},
    "replace_values_in_col": {
        "detailed-label": {
            "-": "Benign"
        },
        "duration": {
            "-": 99
        },
        "orig_bytes": {
            "-": 99
        },
        "resp_bytes": {
            "-": 99
        },
        "missed_bytes": {
            "-": 99
        },
        "local_orig": {
            "-": 99
        },
        "local_resp": {
            "-": 99
        },
        "orig_pkts": {
            "-": 99
        },
        "orig_ip_bytes": {
            "-": 99
        },
        "resp_pkts": {
            "-": 99
        },
        "resp_ip_bytes": {
            "-": 99
        },
    },
    "transform_to_numeric": [
        "duration",
        "orig_bytes",
        "resp_bytes",
        "missed_bytes",
        "local_orig",
        "local_resp",
        "orig_pkts",
        "orig_ip_bytes",
        "resp_pkts",
        "resp_ip_bytes"
    ],
    "class_labels": {
        0: "Benign",
        1: "Att",
        2: "C&C",
        3: "C&C-FD",
        4: "C&C-HB",
        5: "C&C-HB-Att",
        6: "C&C-HB-FD",
        7: "C&C-Mirai",
        8: "C&C-HPS",
        9: "C&C-Torii",
        10: "DDoS",
        11: "FD",
        12: "Okiru",
        13: "Okiru-Att",
        14: "HorizPortSc",
        15: "HorizPortSc-Att",
    },
    "category_encodings": {
        "conn_state": {
            "S0": 0,
            "S1": 1,
            "S2": 2,
            "S3": 3,
            "SF": 4,
            "REJ": 5,
            "RSTO": 6,
            "RSTR": 7,
            "RSTOS0": 8,
            "RSTRH": 9,
            "SH": 10,
            "SHR": 11,
            "OTH": 12
        },
        "detailed-label": {
            "Benign": 0,
            "Attack": 1,
            "C&C": 2,
            "C&C-FileDownload": 3,
            "C&C-HeartBeat": 4,
            "C&C-HeartBeat-Attack": 5,
            "C&C-HeartBeat-FileDownload": 6,
            "C&C-Mirai": 7,
            "C&C-PartOfAHorizontalPortScan": 8,
            "C&C-Torii": 9,
            "DDoS": 10,
            "FileDownload": 11,
            "Okiru": 12,
            "Okiru-Attack": 13,
            "PartOfAHorizontalPortScan": 14,
            "PartOfAHorizontalPortScan-Attack": 15,
        },
        "label": {
            "benign": 0,
            "Malicious": 1
        },
        "proto": {
            "icmp": 0,
            "tcp": 1,
            "udp": 2
        },
        "service": {
            "-": 0,
            "dhcp": 1,
            "dns": 2,
            "http": 3,
            "ssh": 4,
            "ssl": 5,
            "irc": 6
        },
    },
}

feature_selections = {
    # EXP_FL16_FT14_R_ / EXP_FL4_FT14_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h', 'local_orig',
    # 'local_resp', 'missed_bytes',  'tunnel_parents'
    "F14": {
        "description": 'F14',
        "features": [
            'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
            'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
            'history', 'orig_pkts',
            'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes',
            'detailed-label'
        ]},

    # EXP_FL16_FT17_R_ / EXP_FL4_FT17_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h', 'id.resp_h'
    "F17": {
        "description": 'F17',
        "features": [
            'id.orig_p', 'id.resp_p', 'proto',
            'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
            'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
            'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
            'detailed-label'
        ]},

    # EXP_FL16_FT18_R_ / EXP_FL4_FT18_R_
    # All without:
    # 'ts', 'uid', 'label', 'id.orig_h'
    "F18": {
        "description": 'F18',
        "features": [
            'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
            'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
            'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
            'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
            'detailed-label'
        ]},

    # All without:
    # 'ts', 'uid', 'label'
    "F19": {
        "description": 'F19',
        "features": [
            'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
            'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state',
            'local_orig', 'local_resp', 'missed_bytes', 'history', 'orig_pkts',
            'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'tunnel_parents',
            'detailed-label'
        ]},
}

datasets = {
    'S16': [],
    'S04': [
        "Benign.csv",
        "DDoS.csv",
        "Okiru.csv",
        "PartOfAHorizontalPortScan.csv"
    ]
}


def get_data_sample(dataset_name='S04', rows_per_dataset_file=100_000):
    sample_name = dataset_name + ('_R_' + str(format(rows_per_dataset_file, '_d')))
    return {
        "description": sample_name,
        "files": datasets[dataset_name],  # empty => combine all source files
        "max_rows_per_file": rows_per_dataset_file,
        "combined_data_file_name": sample_name + '.csv',
        "clean_data_file_name": sample_name + '_clean.csv'}


def get_feature_selection(experiment_name):
    features_code = experiment_name.split("_", 1)[0]
    return feature_selections[features_code]['features']


def get_train_data_path(file_path):
    return file_path + '_train.csv'


def get_test_data_path(file_path):
    return file_path + '_test.csv'


def format_line(line, new_sep=','):
    line = __replace_whitespaces(line, replace_with=new_sep)
    line = line.rstrip(new_sep) + '\n'
    return line


def __replace_whitespaces(s, replace_with=','):
    return re.sub(r"\s+", replace_with, s)


def get_exp_data_dir(exp_name):
    return exp_name + "//data//"


def get_exp_models_dir(exp_name):
    return exp_name + "//models//"


def get_exp_results_dir(exp_name):
    return exp_name + "//results//"


def get_exp_name(data_combination, feature_selection_name):
    return feature_selection_name + '_' + data_combination['description']


def get_feat_selection_name(experiment_name):
    return experiment_name.split("_S", 1)[0]


def get_data_sample_name(experiment_name):
    return experiment_name.split("_", 1)[1]


def get_data_sample_name_short(experiment_name):
    return experiment_name.split("_")[1]


def get_sample_row_count(experiment_name):
    return float(experiment_name.split("R_", 1)[1])


def decode_labels(keys):
    class_labels = data_cleanup['class_labels']
    labels = [class_labels[key] for key in keys]
    return labels


def decode_cls_label(key):
    return data_cleanup['class_labels'][key]
