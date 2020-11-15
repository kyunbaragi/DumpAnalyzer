import analyzer
import util
from util import DumpRegex
from myrequests.action import AssignSubOwners
from unittest import TestRunner, TestSuite
from . import case


def default_suite():
    suite = TestSuite()
    suite.add_test(case.DefaultCases('system_properties'))
    return suite


def storage_suite():
    suite = TestSuite()
    suite.add_test(case.StorageCases('ntfs_filesystem'))
    suite.add_test(case.StorageCases('sgdisk_failed'))
    suite.add_test(case.StorageCases('blkid_failed'))
    return suite


def usb_suite():
    return TestSuite()


class VoldAnalyzer(analyzer.IssueAnalyzer):
    def __init__(self):
        super().__init__('VOLD', ['yunkyun.han', 'dingul.han'])

    def before(self, issue):
        util.extract_all(issue.directory)

    def analyze(self, issue):
        print('Analyze', issue)
        actions = [AssignSubOwners(issue, self.members)]

        try:
            dumpstates = util.search(issue.directory, DumpRegex.DEFAULT, reverse=True)
            if dumpstates:
                runner = TestRunner(issue=issue, dumpstate=dumpstates[0])
                runner.run(default_suite(), actions)

                if issue.is_voc():
                    runner.run(storage_suite(), actions)
                    # runner.run(usb_suite(), actions)
            else:
                print('No dumpstate!')
        except Exception as e:
            print(e)
        finally:
            return actions
