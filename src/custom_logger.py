import logging

logger = logging.getLogger("app_log")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s : %(levelname)s]:%(message)s')


file_log = logging.FileHandler("app.log")
file_log.setLevel(logging.INFO)
file_log.setFormatter(formatter)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.WARN)
console_logger.setFormatter(formatter)

logger.addHandler(file_log)
logger.addHandler(console_logger)