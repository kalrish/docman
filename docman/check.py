import logging

logger = logging.getLogger(
    __name__,
)


def check_database(bucket, session):
    results = dict(
    )

    count = 0

    s3 = session.client(
        's3',
    )

    paginator = s3.get_paginator(
        'list_objects_v2',
    )

    kwargs = dict(
    )

    kwargs['Bucket'] = bucket

    iterator = paginator.paginate(
        **kwargs,
    )

    for response in iterator:
        contents = response['Contents']

        for content in contents:
            problems = list(
            )

            key = content['Key']

            response = s3.head_object(
                Bucket=bucket,
                Key=key,
            )

            content_type = response['ContentType']

            if content_type == '':
                problem = 'missing Content-Type'

                problems.append(
                    problem,
                )
            elif content_type == 'binary/octet-stream':
                problem = 'generic Content-Type'

                problems.append(
                    problem,
                )

            if problems:
                results[key] = problems

                count = count + 1

    logger.info(
        '%i objects do not comply',
        count,
    )

    return results
