with open('input') as fh:
    print('Part 1:', sum(int(x) // 3 - 2 for x in fh.readlines()))


import itertools as it

with open('input') as fh:
    print('Part 2:', sum(
        sum(it.takewhile((0).__lt__,
                         it.accumulate(it.repeat(None), lambda a, b: a // 3 - 2, initial=int(x)//3 - 2)))
        for x in fh.readlines()
    ))
