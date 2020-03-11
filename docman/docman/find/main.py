import logging

logger = logging.getLogger(
    __name__,
)


def find(bucket, filters, session):
    matchlist = list(
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

            response = s3.get_object_tagging(
                Bucket=bucket,
                Key=key,
            )

            tagset = response['TagSet']

            matches = check_object(
                filters=filters,
                key=key,
                tagset=tagset,
            )

            if matches:
                tags = {
                    tagpair['Key']: tagpair['Value']
                    for tagpair in tagset
                }

                obj = {
                    'Key': key,
                    'Tags': tags,
                }

                matchlist.append(
                    obj,
                )

    return matchlist


def check_object(filters, key, tagset):
    for f in filters:
        result = f.check(
            key=key,
            tagset=tagset,
        )

        if not result:
            return False

    return True
