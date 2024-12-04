import logging
import sys


logger = logging.getLogger()

def initialize_stdout_logger(enable_debug_logging: bool):
    logger.setLevel(logging.DEBUG if enable_debug_logging else logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)