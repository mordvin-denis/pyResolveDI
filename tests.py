import unittest
from pyresolvedi.settings import resolve_dependency_settings
from pyresolvedi.decorators import resolve_dependencies


class Parser:
    def start(self):
        print('Test parser started')


class BaseHistoryManager:
    def push(self, data):
        print('"' + data + '"' + ' pushed to BaseHistoryManager')


class DBHistoryManager(BaseHistoryManager):
    def push(self, data):
        print('"' + data + '"' + ' pushed to DBHistoryManager')


class TestHistoryManager(BaseHistoryManager):
    def push(self, data):
        print('"' + data + '"' + ' pushed to TestHistoryManager')


class ConcreteParser:
    @resolve_dependencies()
    def __init__(self, history):
        self.history = history

    def start(self):
        self.history.push('Concrete parser started')


resolve_dependency_settings['resolve_map']['app'] = {
    'threads_num': 3,
    'parser': ConcreteParser,
    'history': DBHistoryManager
}

resolve_dependency_settings['resolve_map']['test'] = {
    'threads_num': 1,
    'parser': Parser,
    'history': TestHistoryManager
}


@resolve_dependencies('test')
def test_process(name, threads_num, parser, history):
    return name, threads_num, parser, history


class TestScopeTest(unittest.TestCase):

    def testAllInject(self):
        name, threads_num, parser, history = test_process('test_process')
        self.assertEqual(name, 'test_process')
        self.assertEqual(threads_num, 1)
        self.assertIsInstance(parser, Parser)
        self.assertIsInstance(history, TestHistoryManager)

    def testThreadsNotInject(self):
        name, threads_num, parser, history = test_process('test_process', 3)
        self.assertEqual(name, 'test_process')
        self.assertEqual(threads_num, 3)
        self.assertIsInstance(parser, Parser)
        self.assertIsInstance(history, TestHistoryManager)

    def testHistoryObjNotInject(self):
        name, threads_num, parser, history = test_process('test_process', history=BaseHistoryManager())
        self.assertEqual(name, 'test_process')
        self.assertEqual(threads_num, 1)
        self.assertIsInstance(parser, Parser)
        self.assertIsInstance(history, BaseHistoryManager)


@resolve_dependencies('app')
def app_process(name, threads_num, parser, history):
    return name, threads_num, parser, history


class AppScopeTest(unittest.TestCase):

    def testAllInject(self):
        name, threads_num, parser, history = app_process('app_process')
        self.assertEqual(name, 'app_process')
        self.assertEqual(threads_num, 3)
        self.assertIsInstance(parser, ConcreteParser)
        self.assertIsInstance(history, DBHistoryManager)


@resolve_dependencies('app', threads_num=10)
def another_app_process(name, threads_num, parser, history):
    return name, threads_num, parser, history


class AnotherAppScopeTest(unittest.TestCase):

    def testAllInject(self):
        name, threads_num, parser, history = another_app_process('another_app_process')
        self.assertEqual(name, 'another_app_process')
        self.assertEqual(threads_num, 10)
        self.assertIsInstance(parser, ConcreteParser)
        self.assertIsInstance(history, DBHistoryManager)


@resolve_dependencies()
def default_app_process(name, threads_num, parser, history):
    return name, threads_num, parser, history


class DefaultAppScopeTest(unittest.TestCase):

    def testAllInject(self):
        name, threads_num, parser, history = default_app_process('default_app_process')
        self.assertEqual(name, 'default_app_process')
        self.assertEqual(threads_num, 3)
        self.assertIsInstance(parser, ConcreteParser)
        self.assertIsInstance(history, DBHistoryManager)


class DefaultAppWithCommonScopeScopeTest(unittest.TestCase):

    def setUp(self):
        resolve_dependency_settings['common_dependency_scope'] = 'test'

    def tearDown(self):
        resolve_dependency_settings['common_dependency_scope'] = None

    def testAllInject(self):
        name, threads_num, parser, history = default_app_process('default_app_process')
        self.assertEqual(name, 'default_app_process')
        self.assertEqual(threads_num, 1)
        self.assertIsInstance(parser, Parser)
        self.assertIsInstance(history, TestHistoryManager)


if __name__ == '__main__':
    unittest.main()
