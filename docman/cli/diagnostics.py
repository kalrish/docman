import logging
import sys

logger = logging.getLogger(
    __name__,
)


def report(format_string, *args):
    message = format_string.format(
        *args,
    )

    stuff = message + '\n'

    sys.stderr.write(
        stuff,
    )
