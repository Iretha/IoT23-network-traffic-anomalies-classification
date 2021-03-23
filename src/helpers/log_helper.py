import logging
import time


def add_logger(file_name='log.log', level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S', handlers=[
            logging.FileHandler("..\logs\\" + file_name),
            logging.StreamHandler()
        ])


def log_duration(start_time, msg):
    end_time = time.time()
    exec_time_seconds = (end_time - start_time)
    exec_time_minutes = exec_time_seconds / 60
    logging.info(msg + " %s seconds = %s minutes ---" % (exec_time_seconds, exec_time_minutes))
