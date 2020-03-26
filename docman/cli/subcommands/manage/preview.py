import logging

import docman.cli.diagnostics
import docman.cli.subcommands.manage
import docman.manage.preview


class Command(docman.cli.subcommands.manage.Command):
    common_arguments = [
        'change_set_name',
        'stack_name',
    ]
    help = 'create change set'

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
        docman.manage.preview.create_change_set(
            change_set_name=args.change_set_name,
            session=session,
            stack_name=args.stack_name,
            template_path=args.template,
            templates_bucket=args.templates_bucket,
        )

        docman.cli.diagnostics.report(
            'CloudFormation change set {} created successfully',
            args.change_set_name,
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
            '--templates-bucket',
            default=config['aws']['buckets']['cloudformation templates'],
            dest='templates_bucket',
            help='name of S3 bucket to which to upload CloudFormation template',
            metavar='NAME',
        )

        parser.add_argument(
            'template',
            help='path to CloudFormation stack template',
        )
