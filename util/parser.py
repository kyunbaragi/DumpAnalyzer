import re
import copy


class AvocadoSoup:
    def __init__(self, path, encoding='utf-8', flags=0):
        self.path = path
        self.encoding = encoding
        self.flags = flags

    def scoop(self, begin_pattern, end_pattern=None):
        begin, end = False, False
        sources = []
        with open(self.path, encoding=self.encoding) as f:
            # Same with f.xreadlines().
            for line in f:
                if not begin:
                    if re.search(begin_pattern, line, self.flags):
                        sources.append(line.strip())
                        begin = True
                else:
                    sources.append(line.strip())
                    if end_pattern:
                        if re.search(end_pattern, line, self.flags):
                            end = True
                            break
                    else:
                        # Detect empty line and quit.
                        if re.match(r'\r\n|\r|\n', line, self.flags):
                            sources.pop()
                            end = True
                            break

        if begin and end:
            return Avocado(sources, self.flags)
        else:
            return None


class Avocado:
    def __init__(self, strings, flags=0):
        if not isinstance(strings, list):
            raise TypeError('A strings must be a list of str')
        self.strings = strings
        self.flags = flags
        self.cache = dict()

    def _search(self, pattern):
        for index, string in enumerate(self.strings):
            if pattern:
                if re.search(pattern, string, self.flags):
                    # Cache the searched results.
                    self.cache[pattern] = (string, index)
                    return self.cache[pattern]
            else:
                if string.strip() == '':
                    self.cache[pattern] = ('Empty line', index)
                    return self.cache[pattern]
        return None, -1

    def scoop(self, begin_pattern, end_pattern=None):
        # Return easy case first.
        if not self.contains(begin_pattern):
            return None
        if not self.contains(end_pattern):
            return None

        begin_idx = self.cache.get(begin_pattern)[1]
        end_idx = self.cache.get(end_pattern)[1]

        if begin_idx <= end_idx:
            if end_pattern:
                return Avocado(self.strings[begin_idx:end_idx + 1], self.flags)
            else:
                return Avocado(self.strings[begin_idx:end_idx], self.flags)
        else:
            return Avocado(self.strings[begin_idx:], self.flags).scoop(begin_pattern, end_pattern)

    def search(self, pattern):
        if self.cache.get(pattern):
            return self.cache.get(pattern)[0]
        return self._search(pattern)[0]

    def index(self, pattern):
        if self.cache.get(pattern):
            return self.cache.get(pattern)[1]
        return self._search(pattern)[1]

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

    def size(self):
        return len(self.strings)

    def raw(self):
        return copy.deepcopy(self.strings)

    def tostring(self, delimiter='\n'):
        return delimiter.join(self.strings)
