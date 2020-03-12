import argparse
import logging

logger = logging.getLogger(
    __name__,
)


def parser(s):
    level_name = s.upper(
    )

    try:
        level = getattr(
            logging,
            level_name,
        )
    except AttributeError:
        message = 'invalid log level'

        e = argparse.ArgumentTypeError(
            message,
        )

        raise e
    else:
        return level
