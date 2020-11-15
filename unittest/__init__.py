import sys
import contextlib


class SkipTest(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f'SkipTest[reason={self.reason}]'


class _Outcome:
    def __init__(self):
        self.success = True
        self.skipped = []
        self.errors = []

    @contextlib.contextmanager
    def test_part_executor(self, test_case):
        old_success = self.success
        self.success = True
        try:
            yield
        except SkipTest as e:
            self.success = False
            self.skipped.append((test_case, str(e)))
        except:
            exc_info = sys.exc_info()
            self.success = False
            self.errors.append((test_case, exc_info))
            exc_info = None
        finally:
            self.success = self.success and old_success


class TestCase:
    def __init__(self, method_name):
        self._test_method_name = method_name
        try:
            test_method = getattr(self, method_name)
        except AttributeError:
            raise ValueError('no such test method in %s: %s' %
                             (self.__class__, method_name))
        else:
            self._test_method_doc = test_method.__doc__

        self._actions = []
        self.issue = None
        self.dumpstate = None

    def _call_setup(self):
        self.setup()

    def _call_test_method(self, method):
        method()

    def _call_teardown(self):
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self, issue, dumpstate, result):
        # Set member variables delivered from TestRunner.run(...),
        # before calling testMethod.
        self.issue = issue
        self.dumpstate = dumpstate

        outcome = _Outcome()
        try:
            self.outcome = outcome
            with outcome.test_part_executor(self):
                self._call_setup()

            if outcome.success:
                test_method = getattr(self, self._test_method_name)
                with outcome.test_part_executor(self):
                    self._call_test_method(test_method)
                with outcome.test_part_executor(self):
                    self._call_teardown()
        finally:
            result.extend(self._actions)

            # Clear the outcome, no more needed.
            self.outcome = None

    def append_action(self, action):
        self._actions.append(action)

    def skip_test(self, reason):
        """Skip this test."""
        raise SkipTest(reason)

    def skip_if(self, condition, reason):
        if condition:
            self.skip_test(reason)

    def skip_unless(self, condition, reason):
        if not condition:
            self.skip_test(reason)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


class TestSuite:
    def __init__(self):
        self._tests = []

    def add_test(self, test):
        if not callable(test):
            raise TypeError(f'{repr(test)} is not callable')
        if isinstance(test, type) and issubclass(test, (TestCase, TestSuite)):
            raise TypeError('TestCases and TestSuites must be instantiated '
                            'before passing them to addTest()')
        self._tests.append(test)

    def add_tests(self, tests):
        if isinstance(tests, str):
            raise TypeError('tests must be an iterable of tests, not a string')
        for test in tests:
            self.add_test(test)

    def run(self, issue, dumpstate, result):
        for index, test in enumerate(self):
            test(issue, dumpstate, result)

    def __iter__(self):
        return iter(self._tests)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


class TestRunner:
    def __init__(self, issue, dumpstate):
        self.issue = issue
        self.dumpstate = dumpstate

    def run(self, test, result):
        test(self.issue, self.dumpstate, result)
