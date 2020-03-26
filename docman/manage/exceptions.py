class CaanotCleanup(Exception):
    def __init__(self, bucket, key, original_exception):
        self.bucket = bucket
        self.key = key
        self.original_exception = original_exception


class CannotCreateChangeSet(Exception):
    def __init__(self, original_exception, stack_name):
        self.original_exception = original_exception
        self.stack_name = stack_name
