import argparse
import datetime
import logging

logger = logging.getLogger(
    __name__,
)


def parser(s):
    try:
        date = datetime.datetime.strptime(
            s,
            '%Y',
        )
    except ValueError:
        message = 'invalid year'

        e = argparse.ArgumentTypeError(
            message,
        )

        raise e
    else:
        return date
