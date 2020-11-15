import os
import environment
from analyzer import Issue
from analyzer.vold import VoldAnalyzer

STORAGE_SUITE = \
    ['P201111-00000',
     'P201111-00001',
     'P201111-00002',
     'P201111-00003',
     'P201111-00004']

USB_SUITE = \
    ['P201111-00005',
     'P201111-00006',
     'P201111-00007',
     'P201111-00008',
     'P201111-00009']


def run_testcase(analyzer, issue_id):
    print(f'============= Beginning of {issue_id} ============')
    issue_dir = os.path.join(environment.DIR_DOWNLOAD, issue_id)
    issue = Issue(issue_id, issue_dir)
    actions = analyzer.receive(issue)
    for action in actions:
        print(action)
    print(f'==================================================')


def run_testsuite(analyzer, testsuite):
    for issue_id in testsuite:
        run_testcase(analyzer, issue_id)


if __name__ == '__main__':
    vold_analyzer = VoldAnalyzer()
    run_testsuite(vold_analyzer, STORAGE_SUITE)
    run_testsuite(vold_analyzer, USB_SUITE)
