import argparse
import importlib
import logging
import pkgutil

import boto3

import docman.cli
import docman.config

logger = logging.getLogger(
    __name__,
)


def entry_point():
    config = docman.config.load(
    )

    parser = set_up_argument_parser(
        config=config,
    )

    args = parser.parse_args(
    )

    set_up_logging(
        level=args.log_level,
    )

    session = boto3.session.Session(
        profile_name=args.aws_profile,
    )

    instance = args.instance

    exit_code = instance.execute(
        args,
        session,
    )

    exit_code_type = type(
        exit_code,
    )

    exit_code_is_number = exit_code_type == int

    assert exit_code_is_number

    return exit_code


def set_up_argument_parser(config):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '--bucket',
        default=config['aws']['bucket'],
        dest='bucket',
        help='name of S3 bucket',
        metavar='NAME',
    )

    parser.add_argument(
        '-l',
        '--log',
        choices=[
            'critical',
            'debug',
            'error',
            'info',
            'warning',
        ],
        default=config['log'],
        dest='log_level',
        help='log level',
        # metavar='LEVEL',
    )

    parser.add_argument(
        '-p',
        '--profile',
        default=config['aws']['credentials']['parameters']['profile_name'],
        dest='aws_profile',
        help='AWS profile',
    )

    current_path = docman.cli.__path__[0]

    logger.debug(
        'path: %s',
        current_path,
    )

    subparsers = parser.add_subparsers(
        title='subcommands',
        dest='action',
        required=True,
    )

    load_modules(
        base_path=current_path,
        config=config,
        path=[
            'subcommands',
        ],
        subparsers=subparsers,
    )

    return parser


def load_modules(base_path, config, path, subparsers):
    path_dots = '.'.join(
        path,
    )
    path_slashes = base_path + '/' + '/'.join(
        path,
    )

    iterator = pkgutil.iter_modules(
        path=[
            path_slashes,
        ],
    )

    for module_info in iterator:
        module_name = module_info.name

        module_path = f'..{ path_dots }.{ module_name }'

        module = importlib.import_module(
            name=module_path,
            package=__name__,
        )

        parser = subparsers.add_parser(
            module_name,
            help=module.Command.help,
        )

        command = module.Command(
            config,
            parser,
        )

        if module_info.ispkg:
            # subcommand contains subactions or subcommands

            subsubparsers = parser.add_subparsers(
                description=command.description,
                dest='action',
                metavar='SUBCOMMAND',
                required=True,
            )

            new_path = list(
            )
            new_path.extend(
                path,
            )
            new_path.append(
                module_name,
            )

            load_modules(
                base_path=base_path,
                config=config,
                path=new_path,
                subparsers=subsubparsers,
            )
        else:
            parser.set_defaults(
                instance=command,
            )


def set_up_logging(level):
    level_code = level.upper(
    )

    logging_level = getattr(
        logging,
        level_code,
    )

    logging.basicConfig(
        format='%(name)s: %(levelname)s: %(message)s',
        level=logging_level,
    )
