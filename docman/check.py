import logging

logger = logging.getLogger(
    __name__,
)

size_limit = 128000

storage_classes = {
    False: 'STANDARD',
    True: 'STANDARD_IA',
}


def check_content_type(bucket, session):
    results = dict(
    )

    count = 0

    s3 = session.client(
        's3',
    )

    paginator = s3.get_paginator(
        'list_objects_v2',
    )

    iterator = paginator.paginate(
        Bucket=bucket,
    )

    for response in iterator:
        contents = response['Contents']

        for content in contents:
            key = content['Key']

            response = s3.head_object(
                Bucket=bucket,
                Key=key,
            )

            content_type = response['ContentType']

            problem = None

            if content_type == '':
                problem = 'missing Content-Type'
            elif content_type == 'binary/octet-stream':
                problem = 'generic Content-Type'

            if problem:
                results[key] = problem

                count = count + 1

    logger.info(
        '%i objects do not comply',
        count,
    )

    return results


def check_storage_class(bucket, session):
    results = dict(
    )

    s3 = session.client(
        's3',
    )

    paginator = s3.get_paginator(
        'list_objects_v2',
    )

    iterator = paginator.paginate(
        Bucket=bucket,
    )

    for response in iterator:
        contents = response['Contents']

        for content in contents:
            key = content['Key']
            size = content['Size']
            storage_class = content['StorageClass']

            logger.debug(
                '%s: size: %i',
                key,
                size,
            )

            logger.debug(
                '%s: storage class: %s',
                key,
                storage_class,
            )

            too_big = size >= size_limit and storage_class == 'STANDARD'
            too_small = size < size_limit and storage_class == 'STANDARD_IA'

            if too_big:
                results[key] = 'too big'
            elif too_small:
                results[key] = 'too small'

    count = len(
        results,
    )

    logger.info(
        '%i objects do not comply',
        count,
    )

    return results
