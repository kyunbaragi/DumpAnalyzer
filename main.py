import os
import fnmatch
from dumpanalyzer import DumpAnalyzer
from parser import *

TARGET_DIR_PATH = '/Users/yunkyun/PycharmProjects/TestDirectory/'
EXTENSION_FILTER = ['*.log', '*.txt']


def scan_directory(absolute_path, select_filter=None):
    if select_filter is None:
        return os.listdir(absolute_path)

    paths = []
    for ext in select_filter:
        paths += fnmatch.filter(os.listdir(absolute_path), ext)
    return paths


def select_dumpstate():
    print('Which file do you want to analyze?')
    paths = scan_directory(TARGET_DIR_PATH, EXTENSION_FILTER)
    for i, path in enumerate(paths, 1):
        print('{}: {}'.format(i, path))

    select = int(input())
    if select <= 0 or select > len(paths):
        raise Exception('Invalid index, You should answer proper index in list!')

    return TARGET_DIR_PATH + paths[select - 1]  # Return absolute path


# This is the main function in python.
if __name__ == '__main__':
    dumpstate_path = select_dumpstate()

    # TODO: How to make a module?
    unit = DumpAnalyzer('Check SD card status')
    unit.add_parser(PatternParser('Device Mapper', 'dm-')) \
        .add_parser(PatternParser('MOUNT POINT DUMP', '/dev/block',
                                  Args.OPTION_LINE | Args.OPTION_IGNORE | Args.OPTION_COUNT))
    unit.analyze(dumpstate_path)
