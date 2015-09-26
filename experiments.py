from pyresolvedi.decorators import resolve_dependencies
from pyresolvedi.settings import resolve_dependency_settings


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
        print('Parser created')

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
    print("Resolved as: ", name, threads_num, parser, history)
    history.push('test_process started')
    parser.start()
    print('\n\n')


test_process('Test 1')
test_process('Test 2', 3)
test_process('Test 3', history=BaseHistoryManager())


@resolve_dependencies('app')
def app_process(name, threads_num, parser, history):
    print("Resolved as: ", name, threads_num, parser, history)
    history.push('app_process started')
    parser.start()
    print('\n\n')


app_process('Test 4')


@resolve_dependencies('app', threads_num=10)
def another_app_process(name, threads_num, parser, history):
    print("Resolved as: ", name, threads_num, parser, history)
    history.push('another_app_process started')
    parser.start()
    print('\n\n')


another_app_process('Test 5')


@resolve_dependencies()
def default_app_process(name, threads_num, parser, history):
    print("Resolved as: ", name, threads_num, parser, history)
    history.push('default_app_process started')
    parser.start()
    print('\n\n')


default_app_process('Test 6')

resolve_dependency_settings['common_dependency_scope'] = 'test'
default_app_process('Test 7')