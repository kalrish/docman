import logging

logger = logging.getLogger(
    __name__,
)


def update_stack(change_set_name, session, stack_name):
    cloudformation = session.client(
        'cloudformation',
    )

    cloudformation.execute_change_set(
        ChangeSetName=change_set_name,
        StackName=stack_name,
    )
