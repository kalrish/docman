import json
import logging
import sys

import docman.cli.subcommands
import docman.find.main
import docman.find.filters.deductable
import docman.find.filters.years


class Command(docman.cli.subcommands.Command):
    help = 'find documents matching criteria'

    def __init__(self):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

    def execute(self, args, session):
        filters = list(
        )

        if args.only_deductable:
            f = docman.find.filters.deductable.Filter(
            )

            filters.append(
                f,
            )

        if args.years:
            f = docman.find.filters.years.Filter(
                years=args.years,
            )

            filters.append(
                f,
            )

        matches = docman.find.main.find(
            bucket=args.bucket,
            filters=filters,
            session=session,
        )

        count = len(
            matches,
        )

        self.logger.info(
            '%i matches',
            count,
        )

        json.dump(
            fp=sys.stdout,
            indent=4,
            obj=matches,
        )

        sys.stdout.write(
            '\n',
        )

        exit_code = 0

        return exit_code

    def setup(self, config, parser):
        parser.add_argument(
            '--dates',
            dest='date_range',
            help='date range',
            metavar=(
                'START_DATE',
                'END_DATE',
            ),
            nargs=2,
        )

        parser.add_argument(
            '--deductable',
            action='store_true',
            dest='only_deductable',
            help='steuerlich absetzbare Ausgaben finden',
        )

        parser.add_argument(
            '--years',
            dest='years',
            help='which years',
            metavar='YEAR',
            nargs='+',
        )
