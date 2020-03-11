import argparse
import logging

import docman.cli.argparsing
import docman.cli.diagnostics
import docman.globals
import docman.upload.exceptions
import docman.upload.main


class Command(docman.cli.subcommands.CommandGroup):
    description = 'kind of document'
    help = 'upload a document'
    common_arguments_definition = {
        'bank': {
            'flag_short': 'b',
            'flag_long': 'bank',
            'options': {
                'choices': docman.globals.banks,
                'dest': 'bank',
                'help': 'Bank',
                'required': True,
            },
        },
        'date': {
            'flag_short': 'd',
            'flag_long': 'date',
            'options': {
                'dest': 'date',
                'help': 'date',
                'required': True,
                'type': docman.cli.argparsing.date,
            },
        },
    }

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        parser.add_argument(
            '--content-type',
            default=None,
            dest='content_type',
            help='value of Content-Type',  # FIXME: MIME ?
            metavar='VALUE',
        )

        # FIXME: validate input
        parser.add_argument(
            '-y',
            '--year',
            action='append',
            dest='years',
            help='add a year',
            metavar='YEAR',
            required=True,
        )

    def add_common_arguments(self, parser):
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
            for common_argument in self.common_arguments:
                argument = self.__class__.common_arguments_definition[common_argument]

                flag_short = argument['flag_short']
                flag_long = argument['flag_long']

                flag_short = f'-{ flag_short }'
                flag_long = f'--{ flag_long }'

                parser.add_argument(
                    flag_short,
                    flag_long,
                    **argument['options'],
                )

    def execute_common(self, args, key, session, tags):
        if 'bank' in args:
            tag_value = args.bank
            self.logger.debug(
                'tag: %s: value: %s',
                'Bank',
                tag_value,
            )
            tags['Bank'] = tag_value

        if 'date' in args:
            tag_value = args.date.strftime(
                '%Y.%m.%d',
            )
            self.logger.debug(
                'tag: %s: value: %s',
                'date',
                tag_value,
            )
            tags['date'] = tag_value

        tag_value = ' '.join(
            args.years,
        )
        self.logger.debug(
            'tag: %s: value: %s',
            'years',
            tag_value,
        )
        tags['years'] = tag_value

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
                'an object with key {} already exists',
                key,
            )

            exit_code = 1
#        except docman.upload.ContentType:
#            print(
#                'cannot guess Content-Type; please provide --content-type',
#            )
#
#            exit_code = 1
#        except docman.upload.CannotUpload:
#            print(
#                'cannot upload!',
#            )
#
#            exit_code = 1
        else:
            docman.cli.diagnostics.report(
                'document uploaded; key: {}',
                key,
            )

            exit_code = 0

        return exit_code
