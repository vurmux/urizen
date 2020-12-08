#!/usr/bin/env python3

import pkgutil
import importlib
import sys
from inspect import getmembers, isfunction
import urizen as uz


def find_generators(module):
    path_dict = {}
    spec_list = []
    for importer, modname, ispkg in pkgutil.walk_packages(module.__path__):
        import_path = '{}.{}'.format(module.__name__, modname)
        if ispkg:
            spec = pkgutil._get_spec(importer, modname)
            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        elif import_path.startswith('urizen.generators'):
            path_dict[import_path[18:]] = [
                f
                for f in getmembers(sys.modules.get(import_path))
                if isfunction(f[1]) and not f[0].startswith('_')
                and f[1].__module__ == import_path
            ]
    for spec in spec_list:
        del sys.modules[spec.name]
    return path_dict


def construct_generators_tree():
    proto_gens = find_generators(uz)
    gen_tree = {}
    for gen_path, gen_list in proto_gens.items():
        gen_type, gen_module_name = gen_path.split('.')
        if gen_type not in gen_tree:
            gen_tree[gen_type] = {}
        if gen_module_name not in gen_tree[gen_type]:
            gen_tree[gen_type][gen_module_name] = {}
        for gen_name, gen_function in gen_list:
            gen_tree[gen_type][gen_module_name][gen_name] = gen_function
    return gen_tree