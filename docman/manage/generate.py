import json
import logging

import docman.data

logger = logging.getLogger(
    __name__,
)


def generate(bucket_name):
    template_data = docman.data.cft
    database_write_policy_template = docman.data.dbpw

    template_data['Parameters']['BucketName']['Default'] = bucket_name

    resources = template_data['Resources']

    rules = docman.data.rules

    tag_definitions = rules['tags']

    tag_conditions = tags2iam(
        tag_definitions,
    )

    document_types = rules['document types']

    iterator = document_types.items(
    )

    for codename, document_type in iterator:
        resource_name = f'DatabaseWritePolicy{ codename }'

        # FIXME: deep copy
        resource = database_write_policy_template

        resource['Properties']['PolicyName']['Fn::Join'][1][1] = codename

        statement = resource['Properties']['PolicyDocument']['Statement'][0]

        statement['Resource']['Fn::Sub'][1]['Prefix'] = document_type['prefix']
        statement['Resource']['Fn::Sub'][1]['SubKey'] = document_type['sub_key']

        try:
            tags = document_type['tags']
        except KeyError:
            pass
        else:
            conditions = statement['Condition']

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

        resources[resource_name] = resource

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
