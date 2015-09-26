pyResolveDI: experiment library for resolving methods/function dependencies using parameters
=========================

This experimental library resolves not resolved dependencies of called function/methods/class constructors.
(Constructor/method injection).
Library provides decorator and settings:

.. code-block:: python

    >>> from pyresolvedi.decorators import resolve_dependencies
    >>> from pyresolvedi.settings import resolve_dependency_settings
    ...

Small using example. Have some services classes.

.. code-block:: python

    >>> class Parser:
    >>>     def start(self):
    >>>         print('Test parser started')
    >>>
    >>>
    >>> class BaseHistoryManager:
    >>>     def push(self, data):
    >>>         print('"' + data + '"' + ' pushed to BaseHistoryManager')
    >>>
    >>>
    >>> class DBHistoryManager(BaseHistoryManager):
    >>>     def push(self, data):
    >>>         print('"' + data + '"' + ' pushed to DBHistoryManager')
    >>>
    >>>
    >>> class TestHistoryManager(BaseHistoryManager):
    >>>     def push(self, data):
    >>>         print('"' + data + '"' + ' pushed to TestHistoryManager')
    >>>
    >>>
    >>> class ConcreteParser:
    >>>     @resolve_dependencies()
    >>>     def __init__(self, history):
    >>>         self.history = history
    >>>         print('Parser created')
    >>>
    >>>     def start(self):
    >>>         self.history.push('Concrete parser started')
    ...

We should add dependencies to resolve_dependency_settings['resolve_map'] to any scope.

    .. code-block:: python

    >>> resolve_dependency_settings['resolve_map']['app'] = {
    >>>     'threads_num': 3,
    >>>     'parser': ConcreteParser,
    >>>     'history': DBHistoryManager
    >>> }
    >>>
    >>> resolve_dependency_settings['resolve_map']['test'] = {
    >>>     'threads_num': 1,
    >>>     'parser': Parser,
    >>>     'history': TestHistoryManager
    >>> }
    ...

We can add dependency to resolve_dependency_settings in pyresolvedi.settings module or in any module
where we have imported resolve_dependency_settings from pyresolvedi.settings module.

Now we can use resolve_dependencies decorator. We can use first decorator argument to specify scope of dependencies.

.. code-block:: python

    >>> @resolve_dependencies('test')
    >>> def test_process(name, threads_num, parser, history):
    >>>     print("Resolved as: ", name, threads_num, parser, history)
    >>>     history.push('test_process started')
    >>>     parser.start()
    >>>     print('\n\n')
    ...


When we call test_process and not set some arguments they will resolved if it possible.
If dependency is registered as class dependence will resolved as class instance.
If we want to resolve dependency as class, dependency should have camel case name or ends with 'Class'.

.. code-block:: python

    >>> test_process('Test 1')
    >>> test_process('Test 2', 3)
    >>> test_process('Test 3', history=BaseHistoryManager())
    ...

If we not specified scope name in decorator first scope will be used.

.. code-block:: python

    >>> @resolve_dependencies()
    >>> def default_app_process(name, threads_num, parser, history):
    >>>     print("Resolved as: ", name, threads_num, parser, history)
    >>>     history.push('default_app_process started')
    >>>     parser.start()
    >>>     print('\n\n')
    ...

It is possible to change dependency resolving in decorator:

.. code-block:: python

    >>> @resolve_dependencies('app', threads_num=10)
    >>> def another_app_process(name, threads_num, parser, history):
    >>>     pass
    ...


If dependency has own dependencies all we be resolved during object created.

It is possible to set scope name for any value for all function/methods with dependency injection.
It may be good for testing purposes.

.. code-block:: python

    >>> resolve_dependency_settings['common_dependency_scope'] = 'test'
    ...
