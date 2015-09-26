from collections import OrderedDict


resolve_map = OrderedDict()

# may create different scope names with different dependency resolving map
resolve_map['app'] = {
}

resolve_dependency_settings = {
    'resolve_map': resolve_map,

    # If scope name - all dependencies will use this scope name
    'common_dependency_scope': None
}