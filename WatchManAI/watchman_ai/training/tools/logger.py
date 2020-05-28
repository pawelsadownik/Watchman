import logging


def get_logger(log_f_name):
    """
    Returns instance of configured logger.

    :param log_f_name: file to which stdout/stderr will be redirected
    :type log_f_name: str
    :return: logger instance
    :rtype: logging.Logger
    """
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_f_name)
    logger.addHandler(file_handler)

    return logger
