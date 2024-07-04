import time
import logging

from functools import wraps

logger = logging.getLogger(__name__)


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        logger.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))

        return result

    return wrapper