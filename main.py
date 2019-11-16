import os
from dumpanalyzer import DumpAnalyzer
from parser import *

TARGET_DIR_PATH = '/Users/yunkyun/PycharmProjects/TestDirectory/'


def get_dumpstate(directory):
    print('Which file do you want to analyze?')
    paths = os.listdir(directory)
    for idx, path in enumerate(paths, 1):
        print('{}: {}'.format(idx, path))

    index = int(input())
    if index <= 0 or index > len(paths):
        raise Exception('Invalid index, You should answer proper index in list!')

    return directory + paths[index - 1]  # Return absolute path


# This is the main function in python.
if __name__ == '__main__':
    dumpstate_path = get_dumpstate(TARGET_DIR_PATH)

    # TODO: How to make a module?
    unit = DumpAnalyzer('Check SD card status')
    unit.add_parser(PatternParser('MOUNT POINT DUMP', '/dev/block', Args.OPTION_LINE)) \
        # .add_parser(PatternParser('Device Mapper', 'dm'))
    unit.analyze(dumpstate_path)
