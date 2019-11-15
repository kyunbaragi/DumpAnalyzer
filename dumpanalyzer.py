class DumpAnalyzer:
    def __init__(self, tag):
        self.__TAG = tag
        self.__parser_list = []

    def add_parser(self, parser):
        self.__parser_list.append(parser)

    def analyze(self, dumpstate):
        results = ''
        for parser in self.__parser_list:
            results += parser.parse(dumpstate)
        print(results)
        return results
