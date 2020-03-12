import logging

import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'bank',
        'year',
    ]
    help = 'Steuerbescheinigung'

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

    def execute(self, args, session):
        year = args.year.strftime(
            '%Y',
        )

        key = f'Steuerbescheinigungen/{ year }/{ args.bank }.pdf'

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
