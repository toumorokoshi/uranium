import traceback


def log_exception(logger, level):
    """
    log an exception at a specific level

    this should be called during exception handling.
    """
    logger.log(level, traceback.format_exc())
