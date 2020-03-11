class AlreadyExists(Exception):
    def __init__(self, key):
        self.key = key
