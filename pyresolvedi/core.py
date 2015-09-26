from collections import defaultdict
import inspect


cache_of_resolved = defaultdict(dict)


def resolve_dependency(dependency_name, dependency_scope_name=None, additional_resolve_map=None):
    from pyresolvedi.settings import resolve_dependency_settings

    if additional_resolve_map and dependency_name in additional_resolve_map:
        resolved = additional_resolve_map[dependency_name]
    else:
        if resolve_dependency_settings['common_dependency_scope']:
            dependency_scope_name = resolve_dependency_settings['common_dependency_scope']

        elif not dependency_scope_name:
            dependency_scope_name = list(resolve_dependency_settings['resolve_map'].items())[0][0]  # first as default

        if dependency_scope_name in cache_of_resolved:
            if dependency_name in cache_of_resolved[dependency_scope_name]:
                return cache_of_resolved[dependency_scope_name][dependency_name]

        resolved = resolve_dependency_settings['resolve_map'][dependency_scope_name].get(dependency_name)

        cache_of_resolved[dependency_scope_name][dependency_name] = resolved

    return resolved


def resolve_all_dependencies(func, dependency_scope_name, additional_resolve_map, *args, **kwargs):
    result_params = {}

    co_varnames = func.__code__ .co_varnames[:func.__code__ .co_argcount]
    for pos, varname in enumerate(co_varnames):
        if len(args) > pos and args[pos] is not None:
            continue
        if kwargs.get(varname, None) is not None:
            result_params[varname] = kwargs[varname]
            continue

        resolved = resolve_dependency(varname, dependency_scope_name, additional_resolve_map)

        if resolved:
            if inspect.isclass(resolved):
                # argument with class name dependency should start with upper char or finish with 'class' (or 'Class')
                if varname.lower().endswith('class') or varname[0].isupper():
                    resolved_obj = resolved
                else:
                    resolved_obj = resolved()
            else:
                resolved_obj = resolved

            result_params[varname] = resolved_obj
        #else:
            #argspec = inspect.getargspec(func)

    return result_params