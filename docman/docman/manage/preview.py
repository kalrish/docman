import logging

logger = logging.getLogger(
    __name__,
)


def create_change_set(change_set_name, session, stack_name, template_path, templates_bucket):
    s3 = session.client(
        's3',
    )

    f = open(
        template_path,
        'rb',
    )

    key = f'cft/{ change_set_name }'

    s3.put_object(
        Body=f,
        Bucket=templates_bucket,
        Key=key,
    )

    cloudformation = session.client(
        'cloudformation',
    )

    template_url = f'https://{ templates_bucket }.s3.amazonaws.com/{ key }'

    cloudformation.create_change_set(
        Capabilities=[
            'CAPABILITY_NAMED_IAM',
        ],
        ChangeSetName=change_set_name,
        ChangeSetType='UPDATE',
        StackName=stack_name,
        TemplateURL=template_url,
    )

    s3.delete_object(
        Bucket=templates_bucket,
        Key=key,
    )
