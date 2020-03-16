import json
import logging
import sys

import docman.cli.subcommands
import docman.list


class Command(docman.cli.subcommands.Command):
    help = 'list documents'

    def __init__(self):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

    def execute(self, args, session):
        results = docman.list.list_documents(
            bucket=args.bucket,
            include_tags=args.include_tags,
            prefix=args.prefix,
            session=session,
        )

        count = len(
            results,
        )

        self.logger.info(
            '%i documents',
            count,
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
        parser.add_argument(
            '--with-tags',
            action='store_true',
            dest='include_tags',
            help='query and display object tags',
        )

        parser.add_argument(
            '--prefix',
            dest='prefix',
            help='query and display objects under specific prefix',
        )
