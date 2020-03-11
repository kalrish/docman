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

storage_classes = {
    False: 'STANDARD',
    True: 'STANDARD_IA',
}


def upload(bucket, content_type, key, path, session, tags):
    if not content_type:
        # Guess Content-Type based on file name

        return_tuple = mimetypes.guess_type(
            path,
            strict=True,
        )

        mime_type = return_tuple[0]

        logger.debug(
            '%s: guess MIME type: %s',
            path,
            mime_type,
        )

        content_type = mime_type
#        try:
#            content_type = content_type_map[file_name_extension]
#        except KeyError:
#            e = RuntimeError(
#                'cannot determine Content-Type of file',
#            )
#
#            raise e

    if content_type:
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
                    '%s: size: %i',
                    path,
                    size,
                )

                file_is_big = size >= 128000

                storage_class = storage_classes[file_is_big]

                tag_pairs = [
                    f'{key}={value}'
                    for key, value in tags.items()
                ]

                tagging = '&'.join(
                    tag_pairs,
                )

                logger.info(
                    'document %s will be uploaded to %s using storage class %s',
                    path,
                    key,
                    storage_class,
                )

                s3.put_object(
                    Body=f,
                    Bucket=bucket,
                    ContentType=content_type,
                    Key=key,
                    StorageClass=storage_class,
                    Tagging=tagging,
                )
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
