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
OPCODE_OFFSET = '09'
OPCODE_HALT = '99'

MODE_POSITION = '0'
MODE_IMMEDIATE = '1'
MODE_RELATIVE = '2'


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


def read(intcode: List[int], index: int, param_mode: str, rel_base: int = 0) -> int:
    """
    Reads a value from the incode program according to its parameter mode.

    Possible parameter modes are:

    - MODE_POSITION: return the value of the intcode at `index`
    - MODE_IMMEDIATE: return the value of `index` itself
    - MODE_RELATIVE: return the value of the intcode at `index + rel_base`

    >>> read([1002, 4, 3, 4, 33], 3, '0')
    4
    >>> read([1002, 4, 3, 4, 33], 4, '0')
    33
    >>> read([3, 0, 4, 0, 99], 0, '0')
    3

    >>> read([1002, 4, 3, 4, 33], 3, '1')
    3
    >>> read([1002, 4, 3, 4, 33], 5000, '1')
    5000

    >>> read([3, 0, 4, 0, 99], 0, '2', 0) # read from memory address 0 + 0
    3
    >>> read([3, 0, 4, 0, 99], 0, '2', 1) # read from memory address 0 + 1
    0
    >>> read([3, 0, 4, 0, 99], 0, '2', 2) # read from memory address 0 + 2
    4
    >>> read([3, 0, 4, 0, 99], 3, '2', 1) # read from memory address 3 + 1
    99

    >>> read([3, 0, 4, 0, 99], 5, '0') # read from new memory address 5
    0
    >>> read([3, 0, 4, 0, 99], 4, '2', 1) # read from new memory address 4 + 1
    0
    """
    if param_mode == MODE_POSITION:
        extend_memory(intcode, index)
        return intcode[index]
    elif param_mode == MODE_IMMEDIATE:
        return index
    elif param_mode == MODE_RELATIVE:
        extend_memory(intcode, rel_base + index)
        return intcode[rel_base + index]
    else:
        raise Exception('INVALID READ MODE', param_mode)


def write(intcode, index, param_mode, rel_base, value):
    if param_mode == MODE_POSITION:
        extend_memory(intcode, index)
        intcode[index] = value
    elif param_mode == MODE_RELATIVE:
        extend_memory(intcode, rel_base + index)
        intcode[rel_base + index] = value
    else:
        raise Exception('INVALID WRITE MODE', param_mode)


def extend_memory(intcode, target_index):
    if target_index < 0:
        raise Exception('INVALID ADDRESS')

    if target_index >= len(intcode):
        intcode.extend([0] * (target_index - len(intcode) + 1))


def relate(intcode, pointer, p0, rel_base, op):
    p1_mode = p0[-3]
    p1_index = intcode[pointer + 1]
    input_1 = read(intcode, p1_index, p1_mode, rel_base)

    p2_mode = p0[-4]
    p2_index = intcode[pointer + 2]
    input_2 = read(intcode, p2_index, p2_mode, rel_base)

    return op(input_1, input_2)


def jump_if(intcode, pointer, p0, rel_base, op):
    p1_mode = p0[-3]
    p1_index = intcode[pointer + 1]
    p1_value = read(intcode, p1_index, p1_mode, rel_base)

    if op(p1_value, 0):
        p2_mode = p0[-4]
        p2_index = intcode[pointer + 2]
        p2_value = read(intcode, p2_index, p2_mode, rel_base)

        return p2_value


def process_intcode(program: Dict) -> Tuple[bool, int]:
    intcode = program['intcode']

    while (program['pointer'] < len(intcode)):
        pointer = program['pointer']
        rel_base = program['relative_base']
        input_values = program['input_values']

        # Normalizes the format of intcode instructions:
        # 1 → '00001'
        # 1002 → '01002'
        # This ensures that “unset” options default to '0'
        p0 = format(intcode[pointer], '05d')
        opcode = p0[-2:]

        if opcode == OPCODE_HALT:
            program['did_halt'] = True
            return

        if opcode == OPCODE_ADD:
            result = relate(intcode, pointer, p0, rel_base, operator.add)
            p3_index = intcode[pointer + 3]
            p3_mode = p0[-5]
            write(intcode, p3_index, p3_mode, rel_base, result)

            program['pointer'] += 4
        elif opcode == OPCODE_MULTIPLY:
            result = relate(intcode, pointer, p0, rel_base, operator.mul)
            p3_index = intcode[pointer + 3]
            p3_mode = p0[-5]
            write(intcode, p3_index, p3_mode, rel_base, result)

            program['pointer'] += 4
        elif opcode == OPCODE_INPUT:
            p1_mode = p0[-3]
            p1_index = intcode[pointer + 1]
            value = input_values[program['input_pointer']]
            write(intcode, p1_index, p1_mode, rel_base, value)

            program['input_pointer'] += 1
            program['pointer'] += 2
        elif opcode == OPCODE_OUTPUT:
            p1_mode = p0[-3]
            p1_index = intcode[pointer + 1]
            p1_value = read(intcode, p1_index, p1_mode, rel_base)
            program['output'].append(p1_value)

            program['pointer'] += 2
            # Pause execution
            return
        elif opcode == OPCODE_JUMP_IF_TRUE:
            p2_value = jump_if(intcode, pointer, p0, rel_base, operator.ne)

            if p2_value is not None:
                program['pointer'] = p2_value
            else:
                program['pointer'] += 3
        elif opcode == OPCODE_JUMP_IF_FALSE:
            p2_value = jump_if(intcode, pointer, p0, rel_base, operator.eq)

            if p2_value is not None:
                program['pointer'] = p2_value
            else:
                program['pointer'] += 3
        elif opcode == OPCODE_LESS_THAN:
            result = relate(intcode, pointer, p0, rel_base, operator.lt)
            value = 1 if result else 0
            p3_index = intcode[pointer + 3]
            p3_mode = p0[-5]
            write(intcode, p3_index, p3_mode, rel_base, value)

            program['pointer'] += 4
        elif opcode == OPCODE_EQUALS:
            result = relate(intcode, pointer, p0, rel_base, operator.eq)
            value = 1 if result else 0
            p3_index = intcode[pointer + 3]
            p3_mode = p0[-5]
            write(intcode, p3_index, p3_mode, rel_base, value)

            program['pointer'] += 4
        elif opcode == OPCODE_OFFSET:
            p1_index = intcode[pointer + 1]
            p1_mode = p0[-3]
            p1_value = read(intcode, p1_index, p1_mode, rel_base)
            program['relative_base'] += p1_value

            program['pointer'] += 2
        else:
            raise Exception('A very bad thing happened.')


def run_program(intcode, input_values=[]):
    """
    >>> run_program([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    >>> run_program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    [1219070632396864]
    >>> run_program([104, 1125899906842624, 99])
    [1125899906842624]
    """
    program = {
        'intcode': intcode.copy(),
        'pointer': 0,
        'input_values': input_values,
        'input_pointer': 0,
        'relative_base': 0,
        'output': [],
        'did_halt': False
    }

    while not program['did_halt']:
        process_intcode(program)

    return program['output']


def main():
    intcode = read_intcode_program('intcode-program.txt')
    output = run_program(intcode, [1])
    print(output)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
