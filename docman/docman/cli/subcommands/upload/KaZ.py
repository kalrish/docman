import logging

import docman.cli.argparsing
import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'bank',
    ]
    help = 'Kontoauszug'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        superinstance = super(
            Command,
            self,
        )

        superinstance.add_common_arguments(
            parser,
        )

        parser.add_argument(
            '--konto',
            dest='account',
            help='Kontonummer',
            required=True,
        )

        parser.add_argument(
            '--from',
            dest='start_date',
            help='Start date',
            required=True,
            type=docman.cli.argparsing.date,
        )

        parser.add_argument(
            '--to',
            dest='end_date',
            help='End date',
            required=True,
            type=docman.cli.argparsing.date,
        )

    def execute(self, args, session):
        start_date = args.start_date.strftime(
            '%Y-%m-%d',
        )

        end_date = args.end_date.strftime(
            '%Y-%m-%d',
        )

        key = f'Kontoauszüge/{ args.account }/{ start_date }_{ end_date }.pdf'

        tags = dict(
        )

        superinstance = super(
            Command,
            self,
        )

        exit_code = superinstance.execute_common(
            args=args,
            key=key,
            session=session,
            tags=tags,
        )

        return exit_code
