#!/usr/bin/env python3

from typing import List, Tuple
import itertools


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


def process_intcode(intcode: List[int], input_values: List[int] = None):
    """
    >>> process_intcode([3, 0, 4, 0, 99], [1])
    1
    >>> process_intcode([3, 0, 4, 0, 99], [222])
    222
    >>> process_intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8])
    1
    >>> process_intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7])
    0
    >>> process_intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7])
    1
    >>> process_intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8])
    0
    >>> process_intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8])
    1
    >>> process_intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], [1])
    0
    >>> process_intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7])
    1
    >>> process_intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8])
    0
    >>> process_intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0])
    0
    >>> process_intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [1])
    1
    >>> process_intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0])
    0
    >>> process_intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [1])
    1
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [7])
    999
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [8])
    1000
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [9])
    1001
    """

    output = None
    input_counter = 0
    pointer = 0
    while (pointer < len(intcode)):
        param_0 = format(intcode[pointer], '05d')
        opcode = param_0[-2:]

        if opcode == OPCODE_HALT:
            break

        if opcode == OPCODE_ADD:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)

            param_2_mode = param_0[-4:-3]
            input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

            intcode[intcode[pointer + 3]] = input_1 + input_2

            pointer += 4
        elif opcode == OPCODE_MULTIPLY:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)

            param_2_mode = param_0[-4:-3]
            input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

            intcode[intcode[pointer + 3]] = input_1 * input_2

            pointer += 4
        elif opcode == OPCODE_INPUT:
            intcode[intcode[pointer + 1]] = input_values[input_counter]

            pointer += 2
            input_counter += 1
        elif opcode == OPCODE_OUTPUT:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)
            # print(input_1)
            output = input_1

            pointer += 2
        elif opcode == OPCODE_JUMP_IF_TRUE:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)

            if input_1 != 0:
                param_2_mode = param_0[-4:-3]
                input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

                pointer = input_2
            else:
                pointer += 3
        elif opcode == OPCODE_JUMP_IF_FALSE:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)

            if input_1 == 0:
                param_2_mode = param_0[-4:-3]
                input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

                pointer = input_2
            else:
                pointer += 3
        elif opcode == OPCODE_LESS_THAN:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)
            param_2_mode = param_0[-4:-3]
            input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

            intcode[intcode[pointer + 3]] = 1 if input_1 < input_2 else 0

            pointer += 4
        elif opcode == OPCODE_EQUALS:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)
            param_2_mode = param_0[-4:-3]
            input_2 = read(intcode, intcode[pointer + 2], param_2_mode)

            intcode[intcode[pointer + 3]] = 1 if input_1 == input_2 else 0

            pointer += 4
        else:
            raise Exception('A very bad thing happened.')

    return output


def get_thruster_signal(intcode: List[int], phase_inputs: Tuple[int]) -> int:
    """
    >>> get_thruster_signal([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], (4, 3, 2, 1, 0))
    43210
    >>> get_thruster_signal([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], (0, 1, 2, 3, 4))
    54321
    >>> get_thruster_signal([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], (1, 0, 4, 3, 2))
    65210
    """
    output = 0
    for phase_input in phase_inputs:
        output = process_intcode(intcode.copy(), [phase_input, output])
    return output


def find_max_thruster_signal(intcode: List[int]) -> int:
    max_thruster_signal = 0

    for phase_inputs in list(itertools.permutations(range(5), 5)):
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
