import logging
import sys

logger = logging.getLogger(
    __name__,
)


def set_up_logging(everything, level):
    if everything:
        top_logger_name = None
    else:
        top_logger_name = 'docman'

    top_logger = logging.getLogger(
        name=top_logger_name,
    )

    top_logger.setLevel(
        level,
    )

    handler = logging.StreamHandler(
        stream=sys.stderr,
    )

    formatter = logging.Formatter(
        datefmt=None,
        fmt='%(name)s: %(levelname)s: %(message)s',
        style='%',
    )

    handler.setFormatter(
        formatter,
    )

    top_logger.addHandler(
        handler,
    )

#    logging.basicConfig(
#        format='%(name)s: %(levelname)s: %(message)s',
#        level=logging_level,
#    )
