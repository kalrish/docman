import logging
import mimetypes

logger = logging.getLogger(
    __name__,
)


def fix_content_type(bucket, key, session):
    return_tuple = mimetypes.guess_type(
        key,
        strict=True,
    )

    mime_type = return_tuple[0]

    logger.info(
        '%s: guessed MIME type: %s',
        key,
        mime_type,
    )

    s3 = session.client(
        's3',
    )

    response = s3.head_object(
        Bucket=bucket,
        Key=key,
    )

    try:
        storage_class = response['StorageClass']
    except KeyError:
        # HeadObject returns the x-amz-storage-class header
        # only if the object's storage class is not STANDARD
        storage_class = 'STANDARD'

    logger.debug(
        '%s: storage class: %s',
        key,
        storage_class,
    )

    s3.copy_object(
        Bucket=bucket,
        ContentType=mime_type,
        CopySource={
            'Bucket': bucket,
            'Key': key,
        },
        Key=key,
        MetadataDirective='REPLACE',
        StorageClass=storage_class,
        TaggingDirective='COPY',
    )
