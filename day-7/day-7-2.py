#!/usr/bin/env python3

from typing import Dict, List, Tuple
import itertools
import operator


OPCODE_ADD = '01'
OPCODE_MULTIPLY = '02'
OPCODE_INPUT = '03'
OPCODE_OUTPUT = '04'
OPCODE_JUMP_IF_TRUE = '05'
OPCODE_JUMP_IF_FALSE = '06'
OPCODE_LESS_THAN = '07'
OPCODE_EQUALS = '08'
OPCODE_HALT = '99'

MODE_IMMEDIATE = '1'
MODE_POSITION = '0'


def read_file(filename) -> str:
    """
    Reads a text file called “orbit-data.txt”
    and returns a list of strings representing direct orbit relationships.
    """
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/' + filename
    file_content = ''

    with open(dir_path, 'r') as file:
        file_content = file.read()
        file.close()

    return file_content.strip()


def read_intcode_program(filename) -> List[int]:
    return list(map(int, read_file(filename).split(',')))


def read(intcode: List[int], index: int, param_mode: str) -> int:
    """
    Reads a value from the incode program according to its parameter mode.

    Possible parameter modes are:

    - MODE_POSITION: return the value of the intcode at `index`
    - MODE_IMMEDIATE: return the value of `index` itself

    >>> read([1002, 4, 3, 4, 33], 3, '0')
    4
    >>> read([1002, 4, 3, 4, 33], 4, '0')
    33
    >>> read([1002, 4, 3, 4, 33], 3, '1')
    3
    >>> read([3, 0, 4, 0, 99], 0, '0')
    3
    """
    if param_mode == MODE_IMMEDIATE:
        return index
    else:
        # Default to position mode (MODE_POSITION)
        return intcode[index]


def relate(intcode, pointer, param_0, op):
    param_1_mode = param_0[-3]
    param_1_index = intcode[pointer + 1]
    input_1 = read(intcode, param_1_index, param_1_mode)

    param_2_mode = param_0[-4]
    param_2_index = intcode[pointer + 2]
    input_2 = read(intcode, param_2_index, param_2_mode)

    return op(input_1, input_2)


def jump_if(intcode, pointer, param_0, op):
    param_1_mode = param_0[-3]
    param_1_index = intcode[pointer + 1]
    param_1_value = read(intcode, param_1_index, param_1_mode)

    if op(param_1_value, 0):
        param_2_mode = param_0[-4]
        param_2_index = intcode[pointer + 2]
        param_2_value = read(intcode, param_2_index, param_2_mode)

        return param_2_value


def process_intcode(program: Dict, input_values: List[int] = []) -> Tuple[bool, int]:
    intcode = program['intcode']

    while (program['pointer'] < len(intcode)):
        pointer = program['pointer']

        # Normalizes the format of intcode instructions:
        # 1 → '00001'
        # 1002 → '01002'
        # This ensures that “unset” options default to '0'
        param_0 = format(intcode[pointer], '05d')
        opcode = param_0[-2:]

        if opcode == OPCODE_HALT:
            program['did_halt'] = True
            return

        if opcode == OPCODE_ADD:
            result = relate(intcode, pointer, param_0, operator.add)
            intcode[intcode[pointer + 3]] = result

            program['pointer'] += 4
        elif opcode == OPCODE_MULTIPLY:
            result = relate(intcode, pointer, param_0, operator.mul)
            intcode[intcode[pointer + 3]] = result

            program['pointer'] += 4
        elif opcode == OPCODE_INPUT:
            param_1_index = intcode[pointer + 1]
            intcode[param_1_index] = input_values[program['input_pointer']]

            program['pointer'] += 2
            program['input_pointer'] += 1
        elif opcode == OPCODE_OUTPUT:
            param_1_mode = param_0[-3]
            param_1_index = intcode[pointer + 1]
            param_1_value = read(intcode, param_1_index, param_1_mode)
            program['output'].append(param_1_value)

            program['pointer'] += 2
            # Pause execution
            return
        elif opcode == OPCODE_JUMP_IF_TRUE:
            param_2_value = jump_if(intcode, pointer, param_0, operator.ne)

            if param_2_value is not None:
                program['pointer'] = param_2_value
            else:
                program['pointer'] += 3
        elif opcode == OPCODE_JUMP_IF_FALSE:
            param_2_value = jump_if(intcode, pointer, param_0, operator.eq)

            if param_2_value is not None:
                program['pointer'] = param_2_value
            else:
                program['pointer'] += 3
        elif opcode == OPCODE_LESS_THAN:
            result = 1 if relate(intcode, pointer, param_0, operator.lt) else 0
            param_3_index = intcode[pointer + 3]
            intcode[param_3_index] = result

            program['pointer'] += 4
        elif opcode == OPCODE_EQUALS:
            result = 1 if relate(intcode, pointer, param_0, operator.eq) else 0
            param_3_index = intcode[pointer + 3]
            intcode[param_3_index] = result

            program['pointer'] += 4
        else:
            raise Exception('A very bad thing happened.')


def get_thruster_signal(intcode: List[int], inputs: Tuple[int]) -> int:
    """
    >>> get_thruster_signal([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], (9, 8, 7, 6, 5))
    139629729
    >>> get_thruster_signal([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10], (9, 7, 8, 5, 6))
    18216
    """

    program_a = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_pointer': 0,
        'output': [],
        'did_halt': False
    }
    program_b = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_pointer': 0,
        'output': [],
        'did_halt': False
    }
    program_c = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_pointer': 0,
        'output': [],
        'did_halt': False
    }
    program_d = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_pointer': 0,
        'output': [],
        'did_halt': False
    }
    program_e = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_pointer': 0,
        'output': [],
        'did_halt': False
    }

    program_e['output'] = [0]
    program_did_halt = False

    while not program_did_halt:
        process_intcode(program_a, [inputs[0]] + program_e['output'])
        process_intcode(program_b, [inputs[1]] + program_a['output'])
        process_intcode(program_c, [inputs[2]] + program_b['output'])
        process_intcode(program_d, [inputs[3]] + program_c['output'])
        process_intcode(program_e, [inputs[4]] + program_d['output'])

        program_did_halt = program_a['did_halt'] and program_b['did_halt'] and program_c[
            'did_halt'] and program_d['did_halt'] and program_e['did_halt']

    return program_e['output'][-1]


def find_max_thruster_signal(intcode: List[int]) -> int:
    max_thruster_signal = 0

    for phase_inputs in list(itertools.permutations(range(5, 10), 5)):
        thruster_signal = get_thruster_signal(intcode, phase_inputs)

        if thruster_signal > max_thruster_signal:
            max_thruster_signal = thruster_signal

    return max_thruster_signal


def main():
    intcode = read_intcode_program('intcode-program.txt')
    max_thruster_signal = find_max_thruster_signal(intcode)
    print(max_thruster_signal)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
