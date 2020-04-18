import logging


def get_logger(consts):
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # TODO: validate whether pointed path exists
    file_handler = logging.FileHandler(consts.LOG_F_PATH)
    logger.addHandler(file_handler)
    return logger