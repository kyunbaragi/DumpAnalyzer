from abc import *


class Args:
    LINE = 'line'
    COUNT = 'count'
    MATCH = 'match'
    IGNORE = 'ignore'

    def __init__(self, args):
        self.__args = set()

    def has(self, arg):
        return arg in self.__args

    def set(self, arg):
        self.__args.add(arg)


class Parser(metaclass=ABCMeta):
    def __init__(self, tag):
        self.__TAG = tag

    @abstractmethod
    def parse(self, dumpstate):
        pass


class PatternParser(Parser):
    def __init__(self, tag, pattern, options=None):
        super().__init__(tag)
        self.__pattern = pattern
        self.__args = Args(options)

    def parse(self, dumpstate):
        result = ''
        for line in dumpstate:
            pass
        return result


class BlockParser(Parser):
    def __init__(self, tag, pattern, options=None):
        super().__init__(tag)
        self.__pattern = pattern
        self.__options = options

    def parse(self, dumpstate):
        result = ''
        for line in dumpstate:
            pass
        return result
