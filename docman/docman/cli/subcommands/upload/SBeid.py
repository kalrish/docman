import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'year',
    ]

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
        year = args.year.strftime(
            '%Y',
        )

        key = f'{ year }.pdf'

        tags = dict(
        )

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
