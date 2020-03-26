import abc


class CommandGroup(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, parser):
        pass


class Command(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, args, session):
        pass

    @abc.abstractmethod
    def setup(self, config, parser):
        pass
