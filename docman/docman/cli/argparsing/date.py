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
            '%d.%m.%Y',
        )
    except ValueError:
        message = 'invalid date'

        e = argparse.ArgumentTypeError(
            message,
        )

        raise e
    else:
        return date
