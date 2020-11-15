import re


class AvocadoSoup:
    def __init__(self, path, encoding='utf-8', flags=0):
        self.path = path
        self.encoding = encoding
        self.flags = flags

    def scoop(self, fpattern, lpattern=None):
        first, last = False, False
        sources = []
        with open(self.path, encoding=self.encoding) as f:
            # Same with f.xreadlines().
            for line in f:
                if not first:
                    if re.search(fpattern, line, self.flags):
                        sources.append(line.strip())
                        first = True
                else:
                    sources.append(line.strip())
                    if lpattern:
                        if re.search(lpattern, line, self.flags):
                            last = True
                            break
                    else:
                        # Detect empty line and quit.
                        if re.match(r'\r\n|\r|\n', line, self.flags):
                            last = True
                            break

        if first and last:
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
        self.rcache = dict()

    def _search(self, pattern):
        if pattern in self.cache:
            return self.cache.get(pattern)

        match = (None, -1)
        for index, string in enumerate(self.strings):
            if pattern:
                if re.search(pattern, string, self.flags):
                    match = (string, index)
                    break
            else:
                if not string:
                    match = (string, index)
                    break

        self.cache[pattern] = match
        return match

    def _rsearch(self, pattern):
        if pattern in self.rcache:
            return self.rcache.get(pattern)

        match = (None, -1)
        for index, string in enumerate(reversed(self.strings)):
            if pattern:
                if re.search(pattern, string, self.flags):
                    match = (string, self.size() - index - 1)
                    break
            else:
                if not string:
                    match = (string, self.size() - index - 1)
                    break

        self.rcache[pattern] = match
        return match

    def _searchall(self, pattern):
        matches = []
        for string in self.strings:
            if re.search(pattern, string, self.flags):
                matches.append(string)

        return matches

    def _scoop(self, fpattern, lpattern, matches):
        if not self.contains(fpattern):
            return
        if not self.contains(lpattern):
            return

        findex = self.cache.get(fpattern)[1]
        lindex = self.cache.get(lpattern)[1]

        if findex <= lindex:
            matches.append(Avocado(self.strings[findex:lindex + 1], self.flags))
            remains = Avocado(self.strings[lindex + 1:], self.flags)
        else:
            remains = Avocado(self.strings[findex:], self.flags)

        # Recursive call for remained strings.
        return remains._scoop(fpattern, lpattern, matches)

    def scoop(self, fpattern, lpattern=None):
        matches = []
        self._scoop(fpattern, lpattern, matches)
        return matches

    def search(self, pattern):
        return self._search(pattern)[0]

    def index(self, pattern):
        return self._search(pattern)[1]

    def rsearch(self, pattern):
        return self._rsearch(pattern)[0]

    def rindex(self, pattern):
        return self._rsearch(pattern)[1]

    def searchall(self, pattern):
        return self._searchall(pattern)

    def contains(self, pattern):
        return True if self._search(pattern)[0] else False

    def count(self, pattern):
        return len(self._searchall(pattern))

    def size(self):
        return len(self.strings)

    def tostring(self, separator='\n'):
        return separator.join(self.strings)
