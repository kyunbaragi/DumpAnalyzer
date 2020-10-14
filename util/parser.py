import re


class AvocadoSoup:
    def __init__(self, path, encoding='utf8'):
        self.path = path
        self.encoding = encoding

    def scoop(self, begin_pattern, end_pattern, flags=0):
        pass


class Avocado:
    def __init__(self, strings, flags=0):
        if not isinstance(strings, list):
            raise TypeError('A strings must be a list of str')
        self.strings = strings
        self.flags = flags
        self.cache = dict()

    def _search(self, pattern):
        for index, string in enumerate(self.strings):
            if re.search(pattern, string, self.flags):
                # Cache the searched results.
                self.cache[pattern] = (string, index)
                return self.cache[pattern]
        return None, -1

    def scoop(self, begin_pattern, end_pattern):
        # Return easy case first.
        if not self.contains(begin_pattern):
            return None
        if not self.contains(end_pattern):
            return None

        begin_idx = self.cache.get(begin_pattern)
        end_idx = self.cache.get(end_pattern)
        if begin_idx <= end_idx:
            return Avocado(self.strings[begin_idx:end_idx + 1], self.flags)
        else:
            return Avocado(self.strings[begin_idx:], self.flags).scoop(begin_pattern, end_pattern)

    def search(self, pattern):
        if self.cache.get(pattern):
            return self.cache.get(pattern)[0]
        return self._search(pattern)[0]

    def search_all(self, pattern):
        matches = []
        for string in self.strings:
            if re.search(pattern, string, self.flags):
                matches.append(string)
        return matches

    def contains(self, pattern):
        if self.cache.get(pattern):
            return True
        if self._search(pattern)[0]:
            return True
        return False

    def count(self, pattern):
        return len(self.search_all(pattern))

    def text(self):
        return ''.join(self.strings)

    def size(self):
        return len(self.strings)

    def is_empty(self):
        return self.size() == 0
