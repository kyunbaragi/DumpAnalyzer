import os
import abc


class Action(metaclass=abc.ABCMeta):
    def __init__(self, issue):
        self.issue = issue


class PostComment(Action):
    MAX_BYTES = 4000

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
            sources = []
            if self.title:
                sources.append(f'[Title] {self.title}')
            if self.description:
                sources.append(f'[Description] {self.description}')
            if self.cases:
                sources.append(f'[Cases] {self.cases}')
            if self.source:
                sources.append(f'[Source] {self.source}')
            if self.logs:
                sources.append('')
                sources.append(f'{self.logs}')

            # TODO: Truncate the appended string to fit maxbyte.
            return PostComment(self.issue, '\n'.join(sources))

    def __repr__(self):
        return f'PostComment[issue={self.issue}]'


class AssignMainOwner(Action):
    def __init__(self, issue, user_id: str, comment: str = ''):
        super().__init__(issue)
        self.main_owner = {user_id}
        self.comment = comment

    def __repr__(self):
        return f'AssignMainOwner[issue={self.issue}, main_owner={self.main_owner}]'


class AssignSubOwners(Action):
    def __init__(self, issue, user_ids: list, comment: str = ''):
        super().__init__(issue)
        self.sub_owners = set(user_ids)
        self.comment = comment

    def __repr__(self):
        return f'AssignSubOwners[issue={self.issue}, sub_owners={self.sub_owners}]'


class ResolveIssue(Action):
    def __init__(self, issue):
        super().__init__(issue)

    def __repr__(self):
        return f'ResolveIssue[issue={self.issue}]'
