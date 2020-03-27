import json
import logging
import sys

import docman.check
import docman.cli.subcommands


class Command(docman.cli.subcommands.Command):
    help = 'S3 object storage class'

    def __init__(self):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

    def execute(self, args, session):
        results = docman.check.check_storage_class(
            bucket=args.bucket,
            session=session,
        )

        json.dump(
            fp=sys.stdout,
            indent=4,
            obj=results,
        )

        sys.stdout.write(
            '\n',
        )

        exit_code = 0

        return exit_code

    def setup(self, config, parser):
        pass
