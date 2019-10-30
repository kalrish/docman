import boto3
import logging


logger = logging.getLogger(__name__)

# FIXME
bucket = 'paperwork-bucket-1hg4ydzsut0a1'


def main():
    s3 = boto3.client(
        's3',
    )

    keys = list(
    )

    s3_paginator_list_objects_v2 = s3.get_paginator(
        'list_objects_v2',
    )

    s3_list_objects_v2_iterator = s3_paginator_list_objects_v2.paginate(
        Bucket=bucket,
    )

    for s3_list_objects_v2_result in s3_list_objects_v2_iterator:
        keys_portion = [
            obj['Key']
            for obj in s3_list_objects_v2_result['Contents']
        ]

        keys.extend(
            keys_portion,
        )

    for key in keys:
        s3_get_object_tagging_result = s3.get_object_tagging(
            Bucket=bucket,
            Key=key,
        )

        tag_set = s3_get_object_tagging_result['TagSet']

        tags = {
            tag['Key']: tag['Value']
            for tag in tag_set
        }

        if 'Years' in tags:
            if 'years' in tags:
                values_are_equal = tags['years'] == tags['Years']

                assert values_are_equal

                del tags['Years']
            else:
                tags['years'] = tags.pop(
                    'Years',
                )

            new_tag_set = [
                {
                    'Key': key,
                    'Value': value,
                }
                for key, value in tags.items()
            ]

            tagging = {
                'TagSet': new_tag_set,
            }

            print(key)
            print(tag_set)
            print(new_tag_set)
            print('  ')
            print('  ')
            s3.put_object_tagging(
                Bucket=bucket,
                Key=key,
                Tagging=tagging,
            )

    return


def entry_point():
    main()

    return


if __name__ == '__main__':
    entry_point()
