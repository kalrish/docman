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

        logger.error(
            'CloudFormation stack template: cannot upload to S3 (%s/%s): %s',
            templates_bucket,
            key,
            error_code,
        )

        template_body = f.read(
        )

        template_argument['TemplateBody'] = template_body
    else:
        logger.debug(
            'CloudFormation stack template: uploaded to S3 (%s/%s)',
            templates_bucket,
            key,
        )

        template_url = f'https://{ templates_bucket }.s3.amazonaws.com/{ key }'
        template_argument['TemplateURL'] = template_url

        try:
            try:
                response = cloudformation.validate_template(
                    **template_argument,
                )
            except botocore.exceptions.ClientError as original_exception:
                error_code = original_exception.response['Error']['Code']

                logger.critical(
                    'CloudFormation stack template: validation failed: %s',
                    error_code,
                )

                e = docman.manage.exceptions.TemplatedFailedValidation(
                    original_exception=original_exception,
                )

                raise e
            else:
                logger.debug(
                    'CloudFormation stack template: validation passed',
                )

                capabilities = response['Capabilities']

                required_capabilities = ', '.join(
                    capabilities,
                )

                logger.debug(
                    'CloudFormation stack template: required capabilities: %s',
                    required_capabilities,
                )

                iterator = range(
                    2,
                )

                for attempt in iterator:
                    logger.debug(
                        'CloudFormation stack "%s": change set "%s": creation attempt #%i',
                        stack_name,
                        change_set_name,
                        attempt,
                    )

                    try:
                        cloudformation.create_change_set(
                            Capabilities=capabilities,
                            ChangeSetName=change_set_name,
                            ChangeSetType='UPDATE',
                            StackName=stack_name,
                            **template_argument,
                        )
                    except botocore.exceptions.ClientError as original_exception:
                        error_code = original_exception.response['Error']['Code']

                        logger.debug(
                            'CloudFormation stack "%s": change set "%s": cannot create: %s',
                            stack_name,
                            change_set_name,
                            error_code,
                        )

                        if error_code == 'AlreadyExistsException':
                            logger.warning(
                                'CloudFormation stack "%s": change set "%s": already exists',
                                stack_name,
                                change_set_name,
                            )

                            cloudformation.delete_change_set(
                                ChangeSetName=change_set_name,
                                StackName=stack_name,
                            )

                            logger.debug(
                                'CloudFormation stack "%s": change set "%s": deleted',
                                stack_name,
                                change_set_name,
                            )

                            continue
                        else:
                            e = docman.manage.exceptions.CannotCreateChangeSet(
                                original_exception=original_exception,
                                stack_name=stack_name,
                            )

                            raise e
                    else:
                        logger.debug(
                            'CloudFormation stack "%s": change set "%s": creation request succeeded',
                            stack_name,
                            change_set_name,
                        )

                        break
        except Exception as e:
            raise e
        finally:
            try:
                s3.delete_object(
                    Bucket=templates_bucket,
                    Key=key,
                )
            except botocore.exceptions.ClientError as original_exception:
                error_code = original_exception.response['Error']['Code']

                logger.error(
                    'CloudFormation stack template: cannot delete from S3 (%s/%s): %s',
                    templates_bucket,
                    key,
                    error_code,
                )
            except:
                logger.error(
                    'CloudFormation stack template: cannot delete from S3 (%s/%s): unknown error',
                    templates_bucket,
                    key,
                )
            else:
                logger.debug(
                    'CloudFormation stack template: deleted from S3 (%s/%s)',
                    templates_bucket,
                    key,
                )
