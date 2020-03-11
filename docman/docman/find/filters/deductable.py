import logging

import docman.find.filters


class Filter(docman.find.filters.Filter):
    def __init__(self):
        logger_name = f'{ __name__ }.{ Filter.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

    def check(self, key, tagset):
        for tagpair in tagset:
            key = tagpair['Key']
            if key == 'deductable':
                value = tagpair['Value']
                if value == 'yes':
                    return True
                else:
                    return False

        return False
