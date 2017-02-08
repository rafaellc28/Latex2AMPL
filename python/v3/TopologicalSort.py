# from http://stackoverflow.com/questions/15038876/topological-sort-python

from CodeGenerationException import *
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

    isCyclic, name, path_set = cyclic(graph)
    if isCyclic:
        raise CodeGenerationException("It was detected in your code a cyclic dependence including the name '"+ name +"'. Please, correct this problem!")

    for name in graph:
        walk_depth_first(name)

    result = list(takewhile(lambda x: x is not None, (names_by_level.get(i, None) for i in count())))
    result = [item for s in result for item in s]

    return result



# from http://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle
def cyclic(graph):
    visited = set()
    path = [object()]
    path_set = set(path)
    stack = [iter(graph)]
    while stack:
        for v in stack[-1]:
            if v in path_set:
                return True, v, path_set
            elif v not in visited:
                visited.add(v)
                path.append(v)
                path_set.add(v)
                stack.append(iter(graph.get(v, ())))
                break
        else:
            path_set.remove(path.pop())
            stack.pop()
    return False, "", path_set
