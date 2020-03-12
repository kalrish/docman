import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    help = 'Kreditkartenabrechnung'

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

    def execute(self, args):
        return
