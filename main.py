import os
from analyzer.vold import VoldAnalyzer

DIR_DOWNLOAD = '/Users/yunkyun/PycharmProjects/DumpAnalyzer/Download'
SCENARIO_STORAGE = ['CASE_00', 'CASE_01', 'CASE_02', 'CASE_03', 'CASE_04']
SCENARIO_USB = ['CASE_05', 'CASE_06', 'CASE_07', 'CASE_08', 'CASE_09']


class Issue:
    def __init__(self):
        pass


def Run_TestCase(analyzer, issue_id):
    print(f'----------------- Start {issue_id} ---------------')
    issue = Issue()
    issue.id = issue_id
    issue.download_dir = os.path.join(DIR_DOWNLOAD, issue_id)

    actions = analyzer.receive(issue)
    for action in actions:
        print(action)
    print(f'----------------- End {issue_id} -----------------')


def Run_Storage_Scenario(analyzer):
    for issue_id in SCENARIO_STORAGE:
        Run_TestCase(analyzer, issue_id)


def Run_Usb_Scenario(analyzer):
    for issue_id in SCENARIO_USB:
        Run_TestCase(analyzer, issue_id)


if __name__ == '__main__':
    analyzer = VoldAnalyzer
    Run_TestCase(analyzer, 'CASE_00')
    Run_TestCase(analyzer, 'CASE_01')
