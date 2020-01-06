from functools import partial
import itertools as it
import more_itertools as mit
import operator as op

with open('input') as fh:
    initial_state = [int(x) for x in fh.readline().split(',')]

program = initial_state.copy()
inputs = [1]

operations =       {1: op.add, 2: op.mul, 3: inputs.pop, 4: print}
parameter_counts = {1: 2,      2: 2,      3: 0,          4: 1}
program_modifiers = dict.fromkeys((1, 2, 3, 4), partial(op.setitem, program))
index_modifiers = dict.fromkeys((1, 2, 3, 4), lambda i, v: i + 1)
parameter_modes = {0: partial(op.getitem, program), 1: lambda x: x}

def run():
    index = 0
    while index < len(program):
        instruction = str(program[index])
        index += 1
        op_code = int(instruction[-2:])
        if op_code == 99:
            break
        if parameter_counts[op_code]:
            parameters = program[index : index + parameter_counts[op_code]]
            modes = mit.padded(reversed(instruction[:-2]), 0, n=len(parameters))
            parameters = [parameter_modes[int(m)](int(p)) for m, p in zip(modes, parameters)]
            index += parameter_counts[op_code]
        else:
            parameters = ()
        value = operations[op_code](*parameters)
        if value is not None:
            program_modifiers[op_code](program[index], value)
            index = index_modifiers[op_code](index, value)

print('Part 1:')
run()


operations[5] = operations[6] = lambda *args: args
parameter_counts[5] = parameter_counts[6] = 2
program_modifiers[5] = program_modifiers[6] = lambda i, v: None
index_modifiers[5] = lambda i, v: v[1] if v[0] else i
index_modifiers[6] = lambda i, v: v[1] if not v[0] else i

operations[7] = op.lt
operations[8] = op.eq
parameter_counts[7] = parameter_counts[8] = 2
program_modifiers[7] = program_modifiers[8] = partial(op.setitem, program)
index_modifiers[7] = index_modifiers[8] = lambda i, v: i + 1

program[:] = initial_state
inputs[:] = [5]

print('Part 2:')
run()
