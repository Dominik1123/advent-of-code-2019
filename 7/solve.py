from collections import namedtuple
from dataclasses import dataclass
from functools import partial, reduce
import itertools as it
import more_itertools as mit
import operator as op


class Computer:
    Operation = namedtuple('Operation', 'func params state_mod index_mod require_io')
    parameter_modes = {0: op.getitem, 1: lambda p, x: x}
    halt_on = {99}
    halt_after = set()

    def __init__(self):
        self.operations = {}

    def run(self, program, inputs, index=0):
        program = list(program)
        inputs = list(inputs)
        while index < len(program):
            instruction = str(program[index])
            index += 1
            op_code = int(instruction[-2:])
            if op_code in self.halt_on:
                break
            operation = self.operations[op_code]
            if operation.params:
                parameters = program[index : index + operation.params]
                modes = mit.padded(reversed(instruction[:-2]), 0, n=len(parameters))
                parameters = tuple(self.parameter_modes[int(m)](program, int(p)) for m, p in zip(modes, parameters))
                index += operation.params
            else:
                parameters = ()
            if operation.require_io:
                parameters = (inputs,) + parameters
            value = operation.func(*parameters)
            if value is not None:
                operation.state_mod(program, program[index], value)
                index = operation.index_mod(index, value)
            if op_code in self.halt_after:
                break
        return program, inputs, index, op_code

    def register(self, *, code, func, params, state_mod, index_mod, require_io=False):
        self.operations[code] = self.Operation(func, params, state_mod, index_mod, require_io)


computer = Computer()
computer.register(code=1, func=op.add, params=2, state_mod=op.setitem, index_mod=lambda i, v: i + 1)
computer.register(code=2, func=op.mul, params=2, state_mod=op.setitem, index_mod=lambda i, v: i + 1)
computer.register(code=3, func=list.pop, params=0, state_mod=op.setitem, index_mod=lambda i, v: i + 1, require_io=True)
computer.register(code=4, func=list.append, params=1, state_mod=None, index_mod=None, require_io=True)
computer.register(code=5, func=lambda *args: args, params=2, state_mod=lambda *args: None, index_mod=lambda i, v: v[1] if v[0] else i)
computer.register(code=6, func=lambda *args: args, params=2, state_mod=lambda *args: None, index_mod=lambda i, v: v[1] if not v[0] else i)
computer.register(code=7, func=op.lt, params=2, state_mod=op.setitem, index_mod=lambda i, v: i + 1)
computer.register(code=8, func=op.eq, params=2, state_mod=op.setitem, index_mod=lambda i, v: i + 1)


with open('input') as fh:
    initial_state = [int(x) for x in fh.readline().split(',')]


def run_phase_setting(setting):
    return reduce(lambda signal, phase: computer.run(initial_state, (signal, phase))[1][0],
                  setting, 0)

print('Part 1:', max(run_phase_setting(x) for x in it.permutations(range(5))))



def run_feedback_setting(setting, initial_state):
    @dataclass
    class State:
        program: list
        index: int

    states = it.cycle(State(initial_state, 0) for __ in setting)
    setting = iter(setting)
    data, op_code = [0], None
    while op_code not in computer.halt_on:
        state = next(states)
        data.extend(mit.take(1, setting))
        new_state, data, index, op_code = computer.run(state.program, data, state.index)
        state.program = new_state
        state.index = index
    return data[0]

computer.halt_after.add(4)
print('Part 2:', max(run_feedback_setting(x, initial_state) for x in it.permutations(range(5, 10))))
