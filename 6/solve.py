from functools import lru_cache

with open('input') as fh:
    orbits = dict(x.strip().split(')')[::-1] for x in fh)

@lru_cache(maxsize=None)
def number_of_orbits(key):
    try:
        ref = orbits[key]
    except KeyError:
        return 0
    else:
        return number_of_orbits(ref) + 1

print('Part 1:', sum(number_of_orbits(x) for x in orbits))


import networkx as nx

graph = nx.Graph(list(orbits.items()))
print('Part 2:', nx.shortest_path_length(graph, 'YOU', 'SAN') - 2)
