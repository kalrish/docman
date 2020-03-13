import boto3
import logging


logger = logging.getLogger(
    __name__,
)

# FIXME
bucket = 'paperwork-bucket-1hg4ydzsut0a1'


def main():
    s3 = boto3.client(
        's3',
    )

    s3_paginator_list_objects_v2 = s3.get_paginator(
        'list_objects_v2',
    )

    s3_list_objects_v2_iterator = s3_paginator_list_objects_v2.paginate(
        Bucket=bucket,
    )

    for s3_list_objects_v2_result in s3_list_objects_v2_iterator:
        for obj in s3_list_objects_v2_result['Contents']:
            key = obj['Key']

            s3_get_object_tagging_result = s3.get_object_tagging(
                Bucket=bucket,
                Key=key,
            )

            tag_set = s3_get_object_tagging_result['TagSet']

            for tag in tag_set:
                tag_key = tag['Key']
                if tag_key == 'deductable':
                    tag_value = tag['Value']
                    if tag_value == 'yes':
                        print(
                            key,
                        )


def entry_point():
    main(
    )

    return


if __name__ == '__main__':
    entry_point(
    )
