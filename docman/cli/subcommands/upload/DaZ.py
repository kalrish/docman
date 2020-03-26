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

    def execute(self, args):
        return

    def setup(self, config, parser):
        superinstance = super(
        )

        superinstance.setup(
            config,
            parser,
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
