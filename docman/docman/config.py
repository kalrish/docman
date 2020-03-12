import collections
import importlib.resources
import logging

import xdg.BaseDirectory
import yaml

import docman.data

logger = logging.getLogger(
    __name__,
)


def load_defaults():
    f = importlib.resources.open_text(
        encoding='utf-8',
        package='docman.data',
        resource='defaults.yaml',
    )

    document = yaml.safe_load(
        f,
    )

    return document


def merge(source, dest):
    comb = dict(
    )

    for k, v in source.items():
        if isinstance(v, collections.Mapping):
            try:
                dest_value = dest[k]
            except KeyError:
                comb[k] = v
                pass
            else:
                comb[k] = merge(
                    v,
                    dest_value,
                )
        else:
            try:
                dest_value = dest[k]
            except KeyError:
                comb[k] = v
                pass
            else:
                comb[k] = dest_value

    return comb


def load():
    defaults = load_defaults(
    )

    config_dir = xdg.BaseDirectory.save_config_path(
        'docman',
    )
    path = f'{config_dir}/config.yaml'

    try:
        f = open(
            path,
            'r',
        )
    except OSError:
        logger.debug(
            'No configuration file',
        )

        settings = dict(
        )
    else:
        logger.debug(
            'Configuration file at %s opened successfully',
            path,
        )

        settings = yaml.safe_load(
            f,
        )

        logger.debug(
            'Configuration loaded successfully',
        )

    final = merge(
        defaults,
        settings,
    )

    return final
