import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    help = 'Depotauszug'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        parser.add_argument(
            '-f',
            '--format',
            choices=[
                'csv',
                'json',
            ],
            dest='output_format',
            help='output format',
            required=True,
        )

    def execute(self, args):
        return
