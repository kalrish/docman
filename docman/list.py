import logging

logger = logging.getLogger(
    __name__,
)


def list_documents(bucket, include_tags, prefix, session):
    objects = dict(
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

    if prefix:
        kwargs['Prefix'] = prefix

    iterator = paginator.paginate(
        **kwargs,
    )

    for response in iterator:
        contents = response['Contents']

        for content in contents:
            key = content['Key']

            obj = dict(
            )

            obj['Size'] = content['Size']

            if include_tags:
                response = s3.get_object_tagging(
                    Bucket=bucket,
                    Key=key,
                )

                tagset = response['TagSet']

                tags = {
                    tagpair['Key']: tagpair['Value']
                    for tagpair in tagset
                }

                obj['Tags'] = tags

            objects[key] = obj

            count = count + 1

    logger.info(
        '%i documents',
        count,
    )

    return objects
