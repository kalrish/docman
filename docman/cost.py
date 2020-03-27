import json
import logging

import docman.data.regions

logger = logging.getLogger(
    __name__,
)


def estimate(bucket, region, session):
    estimations = dict(
    )

    prices = dict(
    )

    region_name = None

    endpoints = docman.data.regions.get_endpoints(
    )

    partitions = endpoints['partitions']
    for partition in partitions:
        partition_code = partition['partition']
        if partition_code == 'aws':
            regions = partition['regions']
            region_information = regions[region]
            region_name = region_information['description']

    assert region_name

    pricing = session.client(
        region_name='us-east-1',
        service_name='pricing',
    )

    pricing_standard = get_pricing_standard(
        client=pricing,
        region_name=region_name,
    )

    prices['STANDARD'] = pricing_standard

    pricing_standard_ia = get_pricing_standard_ia(
        client=pricing,
        region_name=region_name,
    )

    prices['STANDARD_IA'] = pricing_standard_ia

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

            object_price = prices[storage_class]

            object_cost = object_price * size / 1000000000

            estimations[key] = object_cost

    return estimations


def get_pricing_standard(client, region_name):
    response = client.get_products(
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'ServiceCode',
                'Value': 'AmazonS3',
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': region_name,
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'storageClass',
                'Value': 'General Purpose',
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'volumeType',
                'Value': 'Standard',
            },
        ],
        FormatVersion='aws_v1',
        ServiceCode='AmazonS3',
    )

    assert 'NextToken' not in response

    price_list = response['PriceList']

    assert len(price_list) == 1

    item = price_list[0]

    data = json.loads(
        item,
    )

    price_dimensions = data['terms']['OnDemand']['NRYRNCXF5TWHB476.JRTCKXETXF']['priceDimensions']

    iterator = price_dimensions.items(
    )

    price_per_unit = None

    for code, data in iterator:
        begin_range = data['beginRange']

        if begin_range == '0':
            price_per_unit_s = data['pricePerUnit']['USD']

            price_per_unit = float(
                price_per_unit_s,
            )

            break

    return price_per_unit


def get_pricing_standard_ia(client, region_name):
    response = client.get_products(
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'ServiceCode',
                'Value': 'AmazonS3',
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': region_name,
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'storageClass',
                'Value': 'Infrequent Access',
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'volumeType',
                'Value': 'Standard - Infrequent Access',
            },
        ],
        FormatVersion='aws_v1',
        ServiceCode='AmazonS3',
    )

    assert 'NextToken' not in response

    price_list = response['PriceList']

    assert len(price_list) == 1

    item = price_list[0]

    data = json.loads(
        item,
    )

    price_per_unit_s = data['terms']['OnDemand']['8J8N4Q7B7RUWRJRX.JRTCKXETXF']['priceDimensions']['8J8N4Q7B7RUWRJRX.JRTCKXETXF.6YS6EN2CT7']['pricePerUnit']['USD']

    price_per_unit = float(
        price_per_unit_s,
    )

    return price_per_unit
