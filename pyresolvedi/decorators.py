from pyresolvedi.core import resolve_all_dependencies


class ResolveDependencies(object):
    def __init__(self, dependency_scope_name=None, **kwargs):
        self.kwargs = kwargs
        self.dependency_scope_name = dependency_scope_name

    def __call__(self, original_func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            result_params = resolve_all_dependencies(original_func, decorator_self.dependency_scope_name,
                                                     decorator_self.kwargs, *args, **kwargs)
            return original_func(*args, **result_params)
        return wrappee


resolve_dependencies = ResolveDependencies