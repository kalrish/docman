import logging

import docman.cli.subcommands


class Command(docman.cli.subcommands.Command):
    help = 'download a document'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        parser.add_argument(
            '-o',
            '--output',
            dest='output_path',
            help='path to output file',
            required=True,
        )

    def execute(self, args):
        pass
