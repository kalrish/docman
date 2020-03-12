import argparse
import importlib
import logging
import pkgutil

import boto3

import docman.cli
import docman.cli.argparsing.log_level
import docman.cli.logging
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

    docman.cli.logging.set_up_logging(
        everything=args.log_everything,
        level=args.log_level,
    )

    session = boto3.session.Session(
        profile_name=args.aws_profile,
        region_name=args.aws_region,
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
        default=config['aws']['buckets']['documents'],
        dest='bucket',
        help='name of S3 bucket',
        metavar='NAME',
    )

    parser.add_argument(
        '-l',
        '--log',
        default=config['log'],
        dest='log_level',
        help='log level',
        type=docman.cli.argparsing.log_level.parser,
        metavar='LEVEL',
    )

    parser.add_argument(
        '-L',
        '--log-everything',
        action='store_true',
        default=False,
        dest='log_everything',
        help='emit logs from third-party code too',
    )

    parser.add_argument(
        '--aws-profile',
        default=config['aws']['credentials']['parameters']['profile name'],
        dest='aws_profile',
        help='AWS profile',
    )

    parser.add_argument(
        '--aws-region',
        default=config['aws']['region'],
        dest='aws_region',
        help='AWS region',
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

        if module_info.ispkg:
            # subcommand contains subactions or subcommands

            parser = subparsers.add_parser(
                module_name,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                help=module.CommandGroup.help,
            )

            command = module.CommandGroup(
                config,
                parser,
            )

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
            parser = subparsers.add_parser(
                module_name,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                help=module.Command.help,
            )

            command = module.Command(
                config,
                parser,
            )

            parser.set_defaults(
                instance=command,
            )
