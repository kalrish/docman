import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'bank',
        'date',
    ]
    help = 'Wertpapierabrechnung'
    transaction_type_conversion = {
        'buy': 'Kauf',
        'sell': 'Verkauf',
    }

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
            '--depot',
            dest='depot',
            help='Depotnummer',
            required=True,
        )

        parser.add_argument(
            '--id',
            dest='id',
            help='Rechnungsnummer',
            required=True,
        )

        parser.add_argument(
            '--isin',
            dest='isin',
            help='ISIN (International Securities Identification Number)',
            required=True,
        )

        parser.add_argument(
            '--transaction-type',
            choices=[
                'buy',
                'sell',
            ],
            dest='transaction_type',
            help='Umsatzart',
            required=True,
        )

    def execute(self, args, session):
        key = f'Wertpapierabrechnungen/{ args.depot }/{ args.id }.pdf'

        tags = dict(
        )

        tags['ISIN'] = args.isin
        tags['Umsatzart'] = Command.transaction_type_conversion[args.transaction_type]

        superinstance = super(
        )

        exit_code = superinstance.execute_common(
            args=args,
            key=key,
            session=session,
            tags=tags,
        )

        return exit_code
