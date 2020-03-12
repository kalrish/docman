import logging
import sys

import docman.cli.subcommands.manage
import docman.manage.generate


class Command(docman.cli.subcommands.manage.Command):
    help = 'generate CloudFormation template'

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

        parser.add_argument(
            '-o',
            '--output',
            dest='output_path',
            help='path to output file',
            required=False,
        )

    def execute(self, args, session):
        template = docman.manage.generate.generate(
            bucket_name=args.bucket,
        )

        if args.output_path:
            f = open(
                args.output_path,
                'w',
            )
        else:
            f = sys.stdout

        f.write(
            template,
        )

        exit_code = 0

        return exit_code
