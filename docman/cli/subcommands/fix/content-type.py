import logging

import docman.check
import docman.cli.diagnostics
import docman.cli.subcommands
import docman.fix.content_type


class Command(docman.cli.subcommands.Command):
    help = 'fix Content-Type'

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
        keys = list(
        )

        if args.key:
            keys.append(
                args.key,
            )
        else:
            results = docman.check.check_database(
                bucket=args.bucket,
                session=session,
            )

            iterator = results.items(
            )

            for key, problems in iterator:
                for problem in problems:
                    relevant = problem == 'missing Content-Type' or problem == 'generic Content-Type'
                    if relevant:
                        keys.append(
                            key,
                        )

        count = 0

        for key in keys:
            docman.fix.content_type.fix_content_type(
                bucket=args.bucket,
                key=key,
                session=session,
            )

            count = count + 1

            docman.cli.diagnostics.report(
                '{} fixed',
                key,
            )

        docman.cli.diagnostics.report(
            '{} objects fixed',
            count,
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

        parser.add_argument(
            '--key',
            dest='key',
            help='key of S3 object to fix',
            metavar='KEY',
            required=False,
        )
