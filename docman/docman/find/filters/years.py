import logging

import docman.find.filters


class Filter(docman.find.filters.Filter):
    def __init__(self, years):
        logger_name = f'{ __name__ }.{ Filter.__name__ }'
        self.logger = logging.getLogger(
            logger_name,
        )

        self.years = years

    def check(self, key, tagset):
        for tagpair in tagset:
            tag_key = tagpair['Key']
            if tag_key == 'years':
                tag_value = tagpair['Value']

                self.logger.debug(
                    '%s: `years` tag: %s',
                    key,
                    tag_value,
                )

                document_years = tag_value.split(
                )

                contained = any(
                    item in self.years
                    for item in document_years
                )

                if contained:
                    self.logger.debug(
                        '%s: is contained',
                        key,
                    )

                    return True
                else:
                    self.logger.debug(
                        '%s: is not contained',
                        key,
                    )

                    return False

        self.logger.warning(
            'object %s lacks tag `years`',
            key,
        )

        return False
