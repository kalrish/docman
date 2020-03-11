import datetime
import logging

logger = logging.getLogger(
    __name__,
)


def date(s):
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

    return date
