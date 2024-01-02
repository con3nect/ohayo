import json
from node import node

class functions:
    def __getitem__(self, item):
        return self.function_map[item]

    def dfs(self, function_name, dep = 0):
        print(' '*dep + function_name)
        if (self.function_map[function_name].type not in ['mid', 'extract', 'output']) or self.function_map[function_name].already_run:
            return self.function_map[function_name]
        else:
            if hasattr(self.function_map[function_name], "prework"):
                func = self.function_map[function_name].prework
                func = self.dfs(func, dep+1)
                self.function_map[function_name].prework = func

            if self.function_map[function_name].type in ['extract', 'output'] :
                self.function_map[function_name].already_run = True
                return self.function_map[function_name]

            func_list = self.function_map[function_name].function
            new_func_list = []
            for func in func_list:
                func = self.dfs(func, dep+1)
                new_func_list.append(func)
            self.function_map[function_name].function = new_func_list
            self.function_map[function_name].already_run = True
            return self.function_map[function_name]

    def get_tree_json(self, function_name, dep=0):
        current = {
            "tagName": function_name,
            "attrs": {"fill": "grey"},
            "children": []
        }
        print(function_name)
        if self.function_map[function_name].type == 'leaf':
            current['attrs']['fill'] = 'darkgrey'

        if (self.function_map[function_name].type not in ['mid', 'extract', 'output']):
            self.function_map[function_name].json = current
            return current

        if hasattr(self.function_map[function_name], "prework"):
            func = self.function_map[function_name].prework.name
            func = self.get_tree_json(func, dep+1)
            current['children'] = [func]

        if self.function_map[function_name].type in ['extract', 'output'] :
            self.function_map[function_name].json = current
            return current

        func_list = self.function_map[function_name].function
        for func in func_list:
            func = self.get_tree_json(func.name, dep+1)
            current['children'].append(func)

        self.function_map[function_name].json = current
        return current

    def __init__(self, filename):
        self.function_map={}
        with open(filename, 'r', encoding='utf-8', errors='error') as f:
            data = json.load(f)
        for function in data['function']:
            name = function['name']
            self.function_map[name] = node(function)

        for function in data['function']:
            name = function['name']
            self.dfs(name)


