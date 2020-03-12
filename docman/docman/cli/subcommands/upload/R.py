import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'date',
    ]
    help = 'Rechnung'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        superinstance = super(
        )

        superinstance.__init__(
            config,
            parser,
        )

        parser.add_argument(
            '--deductable',
            choices=[
                'no',
                'yes',
            ],
            dest='deductable',
            help='ob die Ausgabe steuerlich absetzbar ist',
            required=True,
        )

        parser.add_argument(
            '--id',
            dest='id',
            help='Rechnungsnummer',
            required=True,
        )

        parser.add_argument(
            '--merchant',
            dest='merchant',
            help='Händler',
            required=True,
        )

    def execute(self, args, session):
        key = f'Rechnungen/{ args.merchant }/{ args.id }.pdf'

        tags = dict(
        )

        tags['deductable'] = args.deductable

        superinstance = super(
        )

        exit_code = superinstance.execute_common(
            args=args,
            key=key,
            session=session,
            tags=tags,
        )

        return exit_code
