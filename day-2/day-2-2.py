#!/usr/bin/env python3

OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT = 99


puzzle_intcode = [
    1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 19, 5, 23, 1, 13, 23, 27, 1, 27, 6, 31, 2, 31, 6, 35, 2, 6, 35, 39, 1, 39, 5, 43, 1, 13, 43, 47, 1, 6, 47, 51, 2, 13, 51, 55, 1, 10, 55, 59, 1, 59, 5, 63, 1, 10, 63, 67, 1, 67, 5, 71, 1, 71, 10, 75, 1, 9, 75, 79, 2, 13, 79, 83, 1, 9, 83, 87, 2, 87, 13, 91, 1, 10, 91, 95, 1, 95, 9, 99, 1, 13, 99, 103, 2, 103, 13, 107, 1, 107, 10, 111, 2, 10, 111, 115, 1, 115, 9, 119, 2, 119, 6, 123, 1, 5, 123, 127, 1, 5, 127, 131, 1, 10, 131, 135, 1, 135, 6, 139, 1, 10, 139, 143, 1, 143, 6, 147, 2, 147, 13, 151, 1, 5, 151, 155, 1, 155, 5, 159, 1, 159, 2, 163, 1, 163, 9, 0, 99, 2, 14, 0, 0
]

puzzle_output_value = 19690720


def process_intcode_segment(intcode, index):
    opcode = intcode[index]

    if opcode == OPCODE_HALT:
        return

    input_1_index = intcode[index + 1]
    input_2_index = intcode[index + 2]
    output_index = intcode[index + 3]

    if opcode == OPCODE_ADD:
        intcode[output_index] = intcode[input_1_index] + intcode[input_2_index]
    elif opcode == OPCODE_MULTIPLY:
        intcode[output_index] = intcode[input_1_index] * intcode[input_2_index]
    else:
        raise Exception('A very bad thing happened.')


def process_intcode(intcode):
    intcode_copy = intcode.copy()

    for index in range(0, len(intcode_copy), 4):
        if intcode_copy[index] == OPCODE_HALT:
            break

        process_intcode_segment(intcode_copy, index)

    return intcode_copy


def find_noun_verb_combination(intcode, target_output_value):
    """
    >>> find_noun_verb_combination(puzzle_intcode, puzzle_output_value)
    (62, 55)
    """
    for noun in range(0, 100):
        for verb in range(0, 100):
            intcode_copy = intcode.copy()
            intcode_copy[1] = noun
            intcode_copy[2] = verb

            opcode_result = process_intcode(intcode_copy)
            if opcode_result[0] == target_output_value:
                return noun, verb


def main():
    noun, verb = find_noun_verb_combination(
        puzzle_intcode, puzzle_output_value)
    print(100 * noun + verb)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
