import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'bank',
        'date',
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
        date = args.date.strftime(
            '%Y-%m-%d',
        )

        key = f'{ args.depot }/{ date }.pdf'

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

        parser.add_argument(
            '--depot',
            dest='depot',
            help='Depotnummer',
            required=True,
        )
