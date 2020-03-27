import logging
import mimetypes
import os

import botocore

import docman.upload.exceptions

logger = logging.getLogger(
    __name__,
)

content_type_map = {
    'pdf': 'application/pdf',
}

size_limit = 128000

storage_classes = {
    False: 'STANDARD',
    True: 'STANDARD_IA',
}


def upload(bucket, content_type, key, path, session, tags):
    if content_type:
        logger.debug(
            '%s: provided Content-Type: %s',
            path,
            content_type,
        )
    else:
        # Guess Content-Type based on file name

        return_tuple = mimetypes.guess_type(
            path,
            strict=True,
        )

        mime_type = return_tuple[0]

        logger.info(
            '%s: guessed MIME type: %s',
            path,
            mime_type,
        )

        content_type = mime_type

    s3 = session.client(
        's3',
    )

    try:
        s3.head_object(
            Bucket=bucket,
            Key=key,
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.debug(
                'bucket %s does not contain an object with key %s',
                bucket,
                key,
            )

            logger.info(
                '%s: key: %s',
                path,
                key,
            )

            f = open(
                path,
                'rb',
            )

            fd = f.fileno(
            )

            stat_results = os.stat(
                fd,
            )

            size = stat_results.st_size

            logger.debug(
                '%s: size: %i bytes',
                path,
                size,
            )

            file_is_big = size >= size_limit

            storage_class = storage_classes[file_is_big]

            logger.info(
                '%s: storage class: %s',
                path,
                storage_class,
            )

            tag_pairs = list(
            )

            iterator = tags.items(
            )

            for tag_key, tag_value in iterator:
                logger.info(
                    '%s: tag: %s = %s',
                    path,
                    tag_key,
                    tag_value,
                )

                tag_pair = f'{ tag_key }={ tag_value }'

                tag_pairs.append(
                    tag_pair,
                )

            tagging = '&'.join(
                tag_pairs,
            )

            logger.debug(
                '%s: tagging: %s',
                path,
                tagging,
            )

            try:
                s3.put_object(
                    Body=f,
                    Bucket=bucket,
                    ContentType=content_type,
                    Key=key,
                    StorageClass=storage_class,
                    Tagging=tagging,
                )
            except botocore.exceptions.ClientError as original_exception:
                error_code = original_exception.response['Error']['Code']

                logger.error(
                    '%s: PutObject: error: %s',
                    path,
                    error_code,
                )

                if error_code == 'AccessDenied':
                    e = docman.upload.exceptions.AccessDenied(
                        original_exception=original_exception,
                    )

                    raise e
                else:
                    raise original_exception
        else:
            raise e
    else:
        logger.error(
            'bucket %s already contains an object with key %s',
            bucket,
            key,
        )

        e = docman.upload.exceptions.AlreadyExists(
            key=key,
        )

        raise e
