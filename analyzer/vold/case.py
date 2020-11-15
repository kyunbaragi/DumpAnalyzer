from unittest import TestCase
from util.parser import AvocadoSoup
from myrequests.action import PostComment


def build_comment(issue, title, description=None,
                  source=None, cases=None, logs=None):
    builder = PostComment.Builder(issue)
    builder.set_title(title)

    if description:
        builder.set_description(description)
    if source:
        builder.set_source(source)
    if cases:
        builder.set_cases(cases)
    if logs:
        builder.set_logs(logs)

    return builder.build()


class DefaultCases(TestCase):
    def setup(self):
        soup = AvocadoSoup(self.dumpstate, encoding='latin2')
        self.properties = soup.scoop('SYSTEM PROPERTIES', '------')

    def system_properties(self):
        target_props = [
            r'fingerprint',
            r'changelist',
            r'build.id',
        ]

        results = []
        for prop in target_props:
            if self.properties.contains(prop):
                results.append(self.properties.search(prop))

        if results:
            comment = build_comment(
                    issue=self.issue,
                    title='SYSTEM PROPERTIES',
                    source=self.dumpstate,
                    logs='\n'.join(results))

            self.append_action(comment)


class StorageCases(TestCase):
    def setup(self):
        soup = AvocadoSoup(self.dumpstate, encoding='latin2')
        self.stlog = soup.scoop('------ STORAGE BUFFER')

    def ntfs_filesystem(self):
        pass

    def sgdisk_failed(self):
        pass

    def blkid_failed(self):
        pass
