import os
import abc
import util


class Action(metaclass=abc.ABCMeta):
    def __init__(self, issue):
        self.issue = issue


class Comment(Action):
    MAX_BYTES = 4000
    SIGNATURE = 'Commented by Papago.'

    def __init__(self, issue, text):
        super().__init__(issue)
        self.text = text

    class Builder:
        def __init__(self, issue):
            self.issue = issue
            self.title = ''
            self.description = ''
            self.cases = []
            self.source = ''
            self.logs = ''

        def _append(self, source, appended, maxbytes=0):
            if maxbytes:
                if util.calbytes(source) >= maxbytes:
                    return source
                if util.calbytes(source + appended) >= maxbytes:
                    # TODO: Truncate the appended string to fit maxbyte.
                    return source + appended
                else:
                    return source + appended
            else:
                return source + appended

        def set_title(self, title):
            self.title = title.strip()
            return self

        def set_description(self, description):
            self.description = description.strip()
            return self

        def set_cases(self, cases):
            self.cases = cases
            return self

        def set_source(self, source):
            self.source = os.path.basename(source.strip())
            return self

        def set_logs(self, logs):
            self.logs = logs.strip()
            return self

        def build(self):
            text = ''
            usable_bytes = Comment.MAX_BYTES - util.calbytes(Comment.SIGNATURE) - 1
            if self.title:
                text = self._append(text, f'[Title] {self.title}\n', usable_bytes)
            if self.description:
                text = self._append(text, f'[Description] {self.description}\n', usable_bytes)
            if self.cases:
                text = self._append(text, f'[Cases] {self.cases}\n', usable_bytes)
            if self.source:
                text = self._append(text, f'[Source] {self.source}\n', usable_bytes)
            if self.logs:
                text = self._append(text, f'[Logs]\n', usable_bytes)
                text = self._append(text, f'{self.logs}\n', usable_bytes)
            text = self._append(text, '\n')
            text = self._append(text, Comment.SIGNATURE)
            return Comment(self.issue, text)

    def __str__(self):
        return f'<Comment, {self.issue.id}>'


class Assign(Action):
    def __init__(self, issue):
        super().__init__(issue)

    def __str__(self):
        return f'<Assign, {self.issue.id}>'


class Resolve(Action):
    def __init__(self, issue):
        super().__init__(issue)

    def __str__(self):
        return f'<Resolve, {self.issue.id}>'
