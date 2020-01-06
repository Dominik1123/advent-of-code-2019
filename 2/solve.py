import itertools as it
import operator as op

operations = {1: op.add, 2: op.mul}

with open('input') as fh:
    initial_state = [int(x) for x in fh.readline().split(',')]

initial_state[1] = 12
initial_state[2] = 2

def program(memory):
    for i in it.count(step=4):
        o, i, j, k = memory[i:i+4]
        try:
            memory[k] = operations[o](memory[i], memory[j])
        except KeyError as err:
            if o == 99:
                break
            raise
    return memory[0]

print('Part 1:', program(initial_state.copy()))


for noun, verb in it.product(range(100), repeat=2):
    initial_state[1] = noun
    initial_state[2] = verb
    if program(initial_state.copy()) == 19690720:
        break
print('Part 2:', 100*noun + verb)
