#!/usr/bin/env python3

from typing import List


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

puzzle_intcode = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 81, 30, 225, 1102, 9, 63, 225, 1001, 92, 45, 224, 101, -83, 224, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 224, 223, 223, 1102, 41, 38, 225, 1002, 165, 73, 224, 101, -2920, 224, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 18, 14, 224, 1001, 224, -32, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 67, 38, 225, 1102, 54, 62, 224, 1001, 224, -3348, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 1, 224, 1, 224, 223, 223, 1, 161, 169, 224, 101, -62, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 223, 224, 223, 2, 14, 18, 224, 1001, 224, -1890, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 223, 224, 223, 1101, 20, 25, 225, 1102, 40, 11, 225, 1102, 42, 58, 225, 101, 76, 217, 224, 101, -153, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 102, 11, 43, 224, 1001, 224, -451, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223, 1102, 77, 23, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 329, 1001, 223, 1, 223, 7, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 359, 101, 1, 223, 223, 1107, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 374, 101, 1, 223, 223, 1008, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 389, 101, 1, 223, 223, 1007, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 404, 1001, 223, 1, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 419, 1001, 223, 1, 223, 108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 1001, 223, 1, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 464, 101, 1, 223, 223, 107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 479, 101, 1, 223, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 494, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 509, 101, 1, 223, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 524, 1001, 223, 1, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 539, 101, 1, 223, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 554, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 569, 101, 1, 223, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 584, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 599, 1001, 223, 1, 223, 1108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 614, 1001, 223, 1, 223, 1107, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 629, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 101, 1, 223, 223, 8, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 659, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]


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


def process_intcode(intcode: List[int], input_value=None):
    """
    >>> process_intcode([3, 0, 4, 0, 99], 1)
    1
    >>> process_intcode([3, 0, 4, 0, 99], 222)
    222
    >>> process_intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8)
    1
    >>> process_intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7)
    0
    >>> process_intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7)
    1
    >>> process_intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8)
    0
    >>> process_intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8)
    1
    >>> process_intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99], 1)
    0
    >>> process_intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7)
    1
    >>> process_intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8)
    0
    >>> process_intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0)
    0
    >>> process_intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1)
    1
    >>> process_intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0)
    0
    >>> process_intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1)
    1
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 7)
    999
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 8)
    1000
    >>> process_intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 9)
    1001
    """

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
            intcode[intcode[pointer + 1]] = input_value

            pointer += 2
        elif opcode == OPCODE_OUTPUT:
            param_1_mode = param_0[-3:-2]
            input_1 = read(intcode, intcode[pointer + 1], param_1_mode)
            print(input_1)

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


def main():
    process_intcode(puzzle_intcode, 5)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
