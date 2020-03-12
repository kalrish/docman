class AccessDenied(Exception):
    def __init__(self, original_exception):
        self.original_exception = original_exception


class AlreadyExists(Exception):
    def __init__(self, key):
        self.key = key
