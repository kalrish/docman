import logging

import docman.cli.diagnostics


class CommandGroup(docman.cli.subcommands.CommandGroup):
    description = 'management operation'
    help = 'manage backing AWS infrastructure'

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )


class Command(docman.cli.subcommands.Command):
    common_arguments_definition = {
        'change_set_name': {
            'flag_long': 'change-set-name',
            'options': {
                'help': 'name of CloudFormation change set',
                'metavar': 'NAME',
                'required': True,
            },
        },
        'stack_name': {
            'flag_long': 'stack-name',
            'options': {
                'help': 'name of CloudFormation stack',
                'metavar': 'NAME',
                'required': True,
            },
        },
    }

    def __init__(self, config, parser):
        logger_name = f'{ __name__ }.{ Command.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        try:
            common_arguments = self.common_arguments
        except AttributeError:
            pass
        else:
            for common_argument in self.common_arguments:
                argument = self.__class__.common_arguments_definition[common_argument]

                flag_long = argument['flag_long']

                flag_long = f'--{ flag_long }'

                parser.add_argument(
                    flag_long,
                    dest=common_argument,
                    **argument['options'],
                )
