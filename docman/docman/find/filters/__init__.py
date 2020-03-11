import abc


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, key, tagset):
        pass
