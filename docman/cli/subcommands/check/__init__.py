import logging

import docman.cli.subcommands


class CommandGroup(docman.cli.subcommands.CommandGroup):
    description = 'test field'
    help = 'check database'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ CommandGroup.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )
