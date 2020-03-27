import json
import logging

import pkg_resources

logger = logging.getLogger(
    __name__,
)


def get_endpoints():
    f = pkg_resources.resource_stream(
        'botocore',
        'data/endpoints.json',
    )

    endpoints = json.load(
        fp=f,
    )

    return endpoints
