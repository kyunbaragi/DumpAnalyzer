import os
from dumpanalyzer import DumpAnalyzer

TARGET_DIR_PATH = '/Users/yunkyun/PycharmProjects/TestDirectory'


def get_dumpstate(directory):
    paths = os.listdir(directory)
    print('Which file do you want to analyze?')
    for idx, path in enumerate(paths, 1):
        print('{}: {}'.format(idx, path))
    index = int(input())
    return paths[index - 1]


# This is the main function in python.
if __name__ == '__main__':
    dumpstate_path = get_dumpstate(TARGET_DIR_PATH)

    analyzer0 = DumpAnalyzer('dumpsys MOUNT SERVICE')
    analyzer1 = DumpAnalyzer('MMC Error')

