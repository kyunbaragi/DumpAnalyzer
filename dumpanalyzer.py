class DumpAnalyzer:
    def __init__(self, tag):
        self.__TAG = tag
        self.__parser_list = []

    def make_header(self, path):
        return 'Target: {}\n'.format(path) \
                + 'Analyzer: {}\n'.format(self.__TAG)

    def add_parser(self, parser):
        self.__parser_list.append(parser)
        return self

    def analyze(self, dumpstate_path):
        print(self.make_header(dumpstate_path))
        with open(dumpstate_path, "r") as file:
            lines = file.readlines()
            results = ''
            for parser in self.__parser_list:
                # results += parser.parse(lines)
                print(parser.parse(lines))

        # return results
