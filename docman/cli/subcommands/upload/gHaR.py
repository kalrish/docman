import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    def __init__(self):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        superinstance = super(
        )

        superinstance.__init__(
        )

    def execute(self, args, session):
        key = f'{ args.year }/{ args.month }.pdf'

        tags = dict(
        )

        tags['Arbeitgeber'] = args.employer

        superinstance = super(
        )

        exit_code = superinstance.execute_common(
            args=args,
            key=key,
            session=session,
            tags=tags,
        )

        return exit_code

    def setup(self, config, parser):
        superinstance = super(
        )

        superinstance.setup(
            config,
            parser,
        )

        parser.add_argument(
            '--employer',
            choices=[
                'Smaato',
            ],
            dest='employer',
            help='Arbeitgeber',
            required=True,
        )

        parser.add_argument(
            '--month',
            dest='month',
            help='Month',
            required=True,
        )

        parser.add_argument(
            '--year',
            dest='year',
            help='Year',
            required=True,
        )
