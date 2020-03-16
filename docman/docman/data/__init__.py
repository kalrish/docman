import importlib.resources
import logging

import yaml

logger = logging.getLogger(
    __name__,
)

documents = dict(
)


def __getattr__(name):
    file_name = f'{ name }.yaml'

    try:
        document = documents[file_name]
    except KeyError:
        logger.debug(
            '%s: not found in cache',
            name,
        )

        document = load(
            file_name,
        )

        documents[file_name] = document

        logger.debug(
            '%s: cached',
            name,
        )
    else:
        logger.debug(
            '%s: found in cache',
            name,
        )

    return document


def load(name):
    exists = importlib.resources.is_resource(
        name=name,
        package=__name__,
    )

    assert exists

    stream = importlib.resources.open_text(
        encoding='utf-8',
        package=__name__,
        resource=name,
    )

    document = yaml.safe_load(
        stream,
    )

    return document
