import logging

import docman.find.filters


class Filter(docman.find.filters.Filter):
    def __init__(self, key, value):
        logger_name = f'{ __name__ }.{ Filter.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        self.key = key
        self.value = value

    def check(self, key, tagset):
        for tagpair in tagset:
            key = tagpair['Key']
            if key == self.key:
                value = tagpair['Value']
                if value == self.value:
                    return True
                else:
                    return False

        return False
