import os
import traceback


def log_exception(logger, level):
    """
    log an exception at a specific level

    this should be called during exception handling.
    """
    logger.log(level, traceback.format_exc())


def log_multiline(logger, level, msg):
    for l in msg.splitlines():
        logger.log(level, l)


def ensure_file(path):
    """ ensure a file exists at the path specified
    """
    parent_dir = os.path.dirname(path)

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    if not os.path.exists(path):
        open(path, 'w+').close()
