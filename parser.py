from abc import *
import re


class Args:
    OPTION_NONE = 0
    OPTION_LINE = 1 << 1
    OPTION_COUNT = 1 << 2
    OPTION_MATCH = 1 << 3
    OPTION_IGNORE = 1 << 4

    def __init__(self, args):
        self.__args = args

    @staticmethod
    def are_settable_options(settable_options, options):
        return (~settable_options & options) == 0

    def has(self, option):
        return (self.__args & option) != 0

    def add(self, option):
        self.__args |= option


class Parser(metaclass=ABCMeta):
    def __init__(self, tag):
        self.__TAG = tag

    @abstractmethod
    def parse(self, dumpstate):
        pass

    def make_header(self):
        return '--------------- {} ---------------\n' \
            .format(self.__TAG)


class PatternParser(Parser):
    _SETTABLE_OPTIONS = Args.OPTION_LINE | Args.OPTION_COUNT \
            | Args.OPTION_MATCH | Args.OPTION_IGNORE

    def __init__(self, tag, pattern, options=Args.OPTION_NONE):
        if pattern is False:
            raise Exception('Invalid pattern!, Pattern can\'t be empty string.')
        if Args.are_settable_options(PatternParser._SETTABLE_OPTIONS, options) is False:
            raise Exception('Invalid options!, Options not supported by PatternParser.')

        super().__init__(tag)
        self.__pattern = pattern
        self.__args = Args(options)

    def parse(self, dumpstate):
        # Init regex flags.
        flags = 0
        if self.__args.has(Args.OPTION_IGNORE):
            flags |= re.IGNORECASE
        if self.__args.has(Args.OPTION_MATCH):
            # TODO: Set proper flag
            pass

        regex = re.compile(self.__pattern, flags)

        # Iterate dumpstate, line by line.
        hit, result = 0, ''
        for index, line in enumerate(dumpstate, 1):
            if regex.match(line):
                hit += 1
                if self.__args.has(Args.OPTION_LINE):
                    result += '{}: {}'.format(index, line)
                else:
                    result += line

        # Set result by priority.
        if self.__args.has(Args.OPTION_COUNT):
            result = 'pattern count={}\n'.format(hit)
        if hit == 0:
            result = 'Can\'t find Pattern.\n'

        return super().make_header() \
            + result


class BlockParser(Parser):
    def __init__(self, tag, pattern, options=None):
        super().__init__(tag)
        self.__pattern = pattern
        self.__args = Args(options)

    def parse(self, dumpstate):
        result = ''
        for line in dumpstate:
            pass
        return result
