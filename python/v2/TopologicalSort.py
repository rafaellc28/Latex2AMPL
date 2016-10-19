# from http://stackoverflow.com/questions/15038876/topological-sort-python

from collections import defaultdict
from itertools import takewhile, count

def sort_topologically_stackless(graph):
    levels_by_name = {}
    names_by_level = defaultdict(set)

    def add_level_to_name(name, level):
        levels_by_name[name] = level
        names_by_level[level].add(name)


    def walk_depth_first(name):
        stack = [name]
        while(stack):
            name = stack.pop()
            if name in levels_by_name:
                continue

            if name not in graph or not graph[name]:
                level = 0
                add_level_to_name(name, level)
                continue

            children = graph[name]

            children_not_calculated = [child for child in children if child not in levels_by_name]
            if children_not_calculated:
                stack.append(name)
                stack.extend(children_not_calculated)
                continue

            level = 1 + max(levels_by_name[lname] for lname in children)
            add_level_to_name(name, level)

    for name in graph:
        walk_depth_first(name)

    result = list(takewhile(lambda x: x is not None, (names_by_level.get(i, None) for i in count())))
    result = [item for s in result for item in s]

    return result

