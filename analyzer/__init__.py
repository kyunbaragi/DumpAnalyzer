import abc
import re


class Issue:
    def __init__(self, issue_id, directory):
        self.id = issue_id
        self.directory = directory
        self.title = ''
        self.contents = ''
        self.reappearance = ''

    def is_voc(self):
        if re.search(r'\[Samsung Members\]', self.title):
            return True
        return False

    def __repr__(self):
        return f'Issue[id={self.id}]'


class IssueAnalyzer(metaclass=abc.ABCMeta):
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def receive(self, issue):
        try:
            self.before(issue)
            actions = self.analyze(issue)
            self.after(issue)
        except Exception as e:
            print(e)
        else:
            return actions

    def before(self, issue):
        pass

    @abc.abstractmethod
    def analyze(self, issue):
        pass

    def after(self, issue):
        pass

    def __repr__(self):
        return f'IssueAnalyzer[name={self.name}, members={self.members}]'
