import logging

import docman.cli.diagnostics
import docman.cli.subcommands.manage
import docman.manage.update


class Command(docman.cli.subcommands.manage.Command):
    common_arguments = [
        'change_set_name',
        'stack_name',
    ]
    help = 'update CloudFormation stack'

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
        docman.manage.update.update_stack(
            change_set_name=args.change_set_name,
            session=session,
            stack_name=args.stack_name,
        )

        docman.cli.diagnostics.report(
            'CloudFormation stack {} updated successfully',
            args.stack_name,
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
