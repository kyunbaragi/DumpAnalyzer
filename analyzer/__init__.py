import abc


class IssueAnalyzer(metaclass=abc.ABCMeta):
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def receive(self, issue):
        self.before(issue)
        results = self.analyze(issue)
        self.after(issue)
        return results

    def before(self, issue):
        pass

    @abc.abstractmethod
    def analyze(self, issue):
        pass

    def after(self, issue):
        pass
