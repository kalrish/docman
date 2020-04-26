import logging

import docman.cli.argparsing.date
import docman.cli.argparsing.year
import docman.cli.diagnostics
import docman.data
import docman.upload.exceptions
import docman.upload.main


def format_date_tag(date):
    representation = date.strftime(
        '%Y.%m.%d',
    )

    return representation


def format_year_tag(date):
    representation = date.strftime(
        '%Y',
    )

    return representation


def format_years_tag(dates):
    representations = map(
        format_year_tag,
        dates,
    )

    representation = ' '.join(
        representations,
    )

    return representation


class CommandGroup(docman.cli.subcommands.CommandGroup):
    description = 'kind of document'
    help = 'upload documents'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ CommandGroup.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        parser.add_argument(
            '--content-type',
            default=None,
            dest='content_type',
            help='MIME type',
            metavar='VALUE',
        )


class Command(docman.cli.subcommands.Command):
    common_arguments_definition = {
        'bank': {
            'flag_short': 'b',
            'flag_long': 'bank',
            'options': {
                'choices': docman.data.rules['banks'],
                'help': 'Bank',
                'metavar': 'BANK',
                'required': True,
            },
            'tags': {
                'Bank': None,
            },
        },
        'date': {
            'flag_short': 'd',
            'flag_long': 'date',
            'options': {
                'help': 'date',
                'metavar': 'DAY.MONTH.YEAR',
                'required': True,
                'type': docman.cli.argparsing.date.parser,
            },
            'tags': {
                'date': format_date_tag,
                'years': format_year_tag,
            },
        },
        'year': {
            'flag_short': 'y',
            'flag_long': 'year',
            'options': {
                'help': 'year',
                'metavar': 'YEAR',
                'required': True,
                'type': docman.cli.argparsing.year.parser,
            },
            'tags': {
                'years': format_year_tag,
            },
        },
        'years': {
            'flag_short': 'y',
            'flag_long': 'year',
            'options': {
                'action': 'append',
                'help': 'add a year',
                'metavar': 'YEAR',
                'required': True,
                'type': docman.cli.argparsing.year.parser,
            },
            'tags': {
                'years': format_years_tag,
            },
        },
    }

    def __init__(self):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        subclass_module = self.__class__.__module__

        subclass_module_name_parts = subclass_module.rsplit(
            maxsplit=1,
            sep='.',
        )

        subclass_module_name = subclass_module_name_parts[1]

        self.definition = docman.data.rules['document types'][subclass_module_name]

        self.help = self.definition['full name']['singular']

    def execute_common(self, args, key, session, tags):
        try:
            common_arguments = self.common_arguments
        except AttributeError:
            pass
        else:
            for common_argument in common_arguments:
                common_argument_definition = self.__class__.common_arguments_definition[common_argument]

                argument_value = getattr(
                    args,
                    common_argument,
                )

                common_argument_tags = common_argument_definition['tags']

                for tag_key, tag_value_formatter in common_argument_tags.items():
                    if tag_value_formatter:
                        tag_value = tag_value_formatter(
                            argument_value,
                        )
                    else:
                        tag_value = argument_value

                    already_set = tag_key in tags
                    not_already_set = not already_set

                    assert not_already_set

                    self.logger.debug(
                        'tag: %s = %s',
                        tag_key,
                        tag_value,
                    )

                    tags[tag_key] = tag_value

        prefix = self.definition['prefix']

        key = f'{ prefix }/{ key }'

        try:
            docman.upload.main.upload(
                bucket=args.bucket,
                content_type=args.content_type,
                key=key,
                path=args.file,
                session=session,
                tags=tags,
            )
        except KeyError:
            exit_code = 1
        except docman.upload.exceptions.AlreadyExists as e:
            docman.cli.diagnostics.report(
                'An object with key {} already exists',
                e.key,
            )

            exit_code = 1
#        except docman.upload.ContentType:
#            print(
#                'cannot guess Content-Type; please provide --content-type',
#            )
#
#            exit_code = 1
        except docman.upload.exceptions.AccessDenied:
            docman.cli.diagnostics.report(
                'Access denied!',
            )

            exit_code = 1
        else:
            docman.cli.diagnostics.report(
                'Document uploaded to {}/{}',
                args.bucket,
                key,
            )

            exit_code = 0

        return exit_code

    def setup(self, config, parser):
        parser.add_argument(
            'file',
            help='path to the file to upload',
            metavar='PATH',
        )

        try:
            common_arguments = self.common_arguments
        except AttributeError:
            pass
        else:
            for common_argument in common_arguments:
                argument = self.__class__.common_arguments_definition[common_argument]

                flag_short = argument['flag_short']
                flag_long = argument['flag_long']

                flag_short = f'-{ flag_short }'
                flag_long = f'--{ flag_long }'

                parser.add_argument(
                    flag_short,
                    flag_long,
                    dest=common_argument,
                    **argument['options'],
                )
