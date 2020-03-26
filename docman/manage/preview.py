import logging

import botocore.exceptions

import docman.manage.exceptions

logger = logging.getLogger(
    __name__,
)


def create_change_set(change_set_name, session, stack_name, template_path, templates_bucket):
    f = open(
        template_path,
        'rb',
    )

    key = f'cft/{ change_set_name }'

    cloudformation = session.client(
        'cloudformation',
    )

    s3 = session.client(
        's3',
    )

    template_argument = dict(
    )

    try:
        s3.put_object(
            Body=f,
            Bucket=templates_bucket,
            Key=key,
        )
    except botocore.exceptions.ClientError as original_exception:
        error_code = original_exception.response['Error']['Code']

        logger.warning(
            'cannot upload CloudFormation stack template to %s/%s: %s',
            templates_bucket,
            key,
            error_code,
        )

        template_body = f.read(
        )

        template_argument['TemplateBody'] = template_body
    else:
        template_url = f'https://{ templates_bucket }.s3.amazonaws.com/{ key }'
        template_argument['TemplateURL'] = template_url

    try:
        cloudformation.create_change_set(
            Capabilities=[
                'CAPABILITY_NAMED_IAM',
            ],
            ChangeSetName=change_set_name,
            ChangeSetType='UPDATE',
            StackName=stack_name,
            **template_argument,
        )
    except botocore.exceptions.ClientError as original_exception:
        e = docman.manage.exceptions.CannotCreateChangeSet(
            original_exception=original_exception,
            stack_name=stack_name,
        )

        raise e
    else:
        logger.debug(
            'FIXME',
        )
    finally:
        try:
            s3.delete_object(
                Bucket=templates_bucket,
                Key=key,
            )
        except botocore.exceptions.ClientError as original_exception:
            error_code = original_exception.response['Error']['Code']

            logger.warning(
                'cannot delete CloudFormation stack template from bucket %s / %s: %s',
                templates_bucket,
                key,
                error_code,
            )

            e = docman.manage.exceptions.CannotCleanup(
                bucket=templates_bucket,
                key=key,
                original_exception=original_exception,
            )

            raise e
        else:
            logger.debug(
                'CloudFormation stack template deleted from bucket %s / %s',
                templates_bucket,
                key,
            )
