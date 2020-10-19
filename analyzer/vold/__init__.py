import abc
import re
import analyzer
import util
from util.parser import AvocadoSoup


class DumpRegex:
    DEFAULT = [r'dumpstate_*']
    ACT = [r'act_dumpstate_*']


class VoldAnalyzer(analyzer.IssueAnalyzer):
    def __init__(self):
        super().__init__('VOLD', ['yunkyun.han', 'dingul.han'])
        self.stlog = None

    def before(self, issue):
        util.extract_all(issue.download_dir)
        dumpstates = util.search(issue.download_dir, DumpRegex.DEFAULT, re.I)

        soup = AvocadoSoup(dumpstates[0], encoding='latin2')
        self.stlog = soup.scoop('------ STORAGE BUFFER')

    def analyze(self, issue):
        pass

    def after(self, issue):
        self.stlog = None


class Case(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def hit(self):
        pass

    @abc.abstractmethod
    def comments(self):
        pass


class NtfsFileSystem(Case):
    def __init__(self):
        super().__init__()

    def hit(self):
        return True

    def comments(self):
        return None


class SgdiskError(Case):
    def __init__(self):
        super().__init__()

    def hit(self):
        return True

    def comments(self):
        return None


class BlkidError(Case):
    def __init__(self):
        super().__init__()

    def hit(self):
        return True

    def comments(self):
        return None


class FsckError(Case):
    def __init__(self):
        super().__init__()

    def hit(self):
        return True

    def comments(self):
        return None
