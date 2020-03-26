import logging

import docman.cli.argparsing.date
import docman.cli.subcommands.upload


class Command(docman.cli.subcommands.upload.Command):
    common_arguments = [
        'bank',
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
        start_date = args.start_date.strftime(
            '%Y-%m-%d',
        )

        end_date = args.end_date.strftime(
            '%Y-%m-%d',
        )

        key = f'{ args.credit_card }/{ start_date }_{ end_date }.pdf'

        tags = dict(
        )

        start_year_s = args.start_date.strftime(
            '%Y',
        )

        start_year = args.start_date.year
        end_year = args.end_date.year

        if start_year == end_year:
            years_tag_value = start_year_s
        else:
            end_year_s = args.end_date.strftime(
                '%Y',
            )

            years_tag_value = f'{ start_year_s } { end_year_s }'

        tags['years'] = years_tag_value

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
            '--credit-card',
            dest='credit_card',
            help='Kreditkartenname',
            required=True,
        )

        parser.add_argument(
            '--from',
            dest='start_date',
            help='Start date',
            required=True,
            type=docman.cli.argparsing.date.parser,
        )

        parser.add_argument(
            '--to',
            dest='end_date',
            help='End date',
            required=True,
            type=docman.cli.argparsing.date.parser,
        )
