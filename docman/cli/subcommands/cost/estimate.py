import functools
import json
import logging
import sys

import docman.cli.subcommands
import docman.cost


class Command(docman.cli.subcommands.Command):
    help = 'estimate monthly database cost'

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
        estimations = dict(
        )

        per_object_estimations = docman.cost.estimate(
            bucket=args.bucket,
            region=args.aws_region,
            session=session,
        )

        estimations['per-object'] = per_object_estimations

        iterator = per_object_estimations.values(
        )

        total_cost = functools.reduce(
            lambda a, b : a+b,
            iterator,
        )

        estimations['total'] = total_cost

        json.dump(
            fp=sys.stdout,
            indent=4,
            obj=estimations,
        )

        sys.stdout.write(
            '\n',
        )

        exit_code = 0

        return exit_code

    def setup(self, config, parser):
        superinstance = super(
        )

        superinstance.setup(
            config,
            parser,
        )
