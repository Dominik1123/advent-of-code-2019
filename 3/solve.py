from functools import reduce
import itertools as it
import numpy as np

with open('input') as fh:
    path_1 = fh.readline().split(',')
    path_2 = fh.readline().split(',')

direction_index = {'U': -1, 'D': -1, 'L': 1, 'R': 1}
direction_increment = {'U': 1, 'D': -1, 'L': -1, 'R': 1}

def compute_locations(path) -> list:
    increments = it.starmap(
        lambda direction, dist: np.stack((direction_increment[direction] * (np.arange(dist) + 1),
                                          np.zeros(dist, dtype=int))[::direction_index[direction]], axis=1),
        map(lambda p: (p[0], int(p[1:])), path)
    )
    return [tuple(xy) for xy in reduce(
        lambda loc, move: np.concatenate((loc, loc[-1] + move)),
        increments,
        np.zeros((1, 2), dtype=int)
    )]

locs_1 = compute_locations(path_1)
locs_2 = compute_locations(path_2)
crossings = set(locs_1) & set(locs_2) - {(0, 0)}

print('Part 1:', min(map(lambda xy: sum(abs(z) for z in xy), crossings)))
print('Part 2:', min(map(lambda xy: locs_1.index(xy) + locs_2.index(xy), crossings)))
