import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    help = 'Gehaltsabrechnung'

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

    def execute(self, args, session):
        key = f'Gehaltsabrechnungen/{ args.year }/{ args.month }.pdf'

        tags = dict(
        )

        tags['Arbeitgeber'] = args.employer

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
