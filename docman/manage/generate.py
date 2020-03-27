import json
import logging

import docman.data

logger = logging.getLogger(
    __name__,
)

upload_actions = [
    's3:PutObject',
    's3:PutObjectTagging',
]


def generate(bucket_name):
    template_data = docman.data.cft

    template_data['Parameters']['BucketName']['Default'] = bucket_name

    statements = template_data['Resources']['DatabaseWritePolicy']['Properties']['PolicyDocument']['Statement']

    rules = docman.data.rules

    tag_definitions = rules['tags']

    tag_conditions = tags2iam(
        tag_definitions,
    )

    allowed_extensions = rules['allowed file name extensions']

    document_types = rules['document types']

    iterator = document_types.items(
    )

    for codename, document_type in iterator:
        statement = dict(
        )

        statement['Sid'] = codename

        statement['Action'] = upload_actions

        prefix = document_type['prefix']
        sub_key = document_type['sub_key']

        resources = list(
        )

        for allowed_extension in allowed_extensions:
            resource = {
                'Fn::Sub': f'${{Bucket.Arn}}/{ prefix }/{ sub_key }.{ allowed_extension }'
            }

            resources.append(
                resource,
            )

        statement['Resource'] = resources

        try:
            tags = document_type['tags']
        except KeyError:
            pass
        else:
            conditions = dict(
            )

            tag_keys = list(
            )

            for tag in tags:
                tag_definition = tag_definitions[tag]

                tag_key = tag_definition['key']

                tag_keys.append(
                    tag_key,
                )

                tag_condition = tag_conditions[tag]

                for condition_type, content in tag_condition.items():
                    try:
                        lala = conditions[condition_type]
                    except KeyError:
                        lala = dict(
                        )
                        conditions[condition_type] = lala

                    for k, v in content.items():
                        lala[k] = v

            conditions['ForAllValues:StringEquals'] = {
                's3:RequestObjectTagKeys': tag_keys,
            }

            statement['Condition'] = conditions

        statement['Effect'] = 'Allow'

        statements.append(
            statement,
        )

    template = json.dumps(
        obj=template_data,
    )

    return template


def tags2iam(definitions):
    iam = dict(
    )

    iterator = definitions.items(
    )

    for codename, definition in iterator:
        conditions = dict(
        )

        key = definition['key']

        try:
            values = definition['values']
        except KeyError:
            pass
        else:
            conditions['StringEquals'] = {
                f's3:RequestObjectTag/{ key }': values,
            }

        try:
            patterns = definition['patterns']
        except KeyError:
            pass
        else:
            conditions['StringLike'] = {
                f's3:RequestObjectTag/{ key }': patterns,
            }

        iam[codename] = conditions

    return iam
