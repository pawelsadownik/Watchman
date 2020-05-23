import logging


def get_logger(log_f_name):
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_f_name)
    logger.addHandler(file_handler)

    return logger