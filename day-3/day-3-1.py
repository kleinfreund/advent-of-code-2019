#!/usr/bin/env python3

import math

CHAR_CENTRAL_PORT = '⊙'
CHAR_CROSS = '╳'
CHAR_BLANK = '·'
WIRE_H = '─'
WIRE_V = '│'
WIRE_DR = '┌'
WIRE_DL = '┐'
WIRE_UR = '└'
WIRE_UL = '┘'
WIRE_CHARS = [WIRE_H, WIRE_V, WIRE_DR, WIRE_DL, WIRE_UR, WIRE_UL]
CORNER_CHARS = [WIRE_DR, WIRE_DL, WIRE_UR, WIRE_UL]

OUTPUT_FILE_NAME = 'schematics.html'
OUTPUT_FILE_PREFIX = """
<style>
body {
    background-color: #0f0f23;
    color: #cccccc;
}

pre {
    display: inline-block;
    transform-origin: 0 0;
    line-height: 1;
    border: 1px solid #333340;
    background-color: #10101a;
    font-family: monospace;
}

.input-4 {
    transform: scale(0.1);
}

.intersection {
    color: #f00;
    text-shadow: 0 0 2px #f00;
}

.central-port {
    color: #ff0;
    text-shadow: 0 0 2px #ff0;
}
</style>
"""


wires = [
    {
        'enabled': True,
        'wire_1': 'R8,U5,L5,D3',
        'wire_2': 'U7,R6,D4,L4',
        'index': '1',
        'manhatten_distance': 6,
        'board_size': {
            'x': 10,
            'y': 11,
        },
        'central_port': {
            'x': 8,
            'y': 1,
        }
    },
    {
        'enabled': True,
        'wire_1': 'R75,D30,R83,U83,L12,D49,R71,U7,L72',
        'wire_2': 'U62,R66,U55,R34,D71,R55,D58,R83',
        'index': '2',
        'manhatten_distance': 159,
        'board_size': {
            'x': 150,
            'y': 241,
        },
        'central_port': {
            'x': 118,
            'y': 1,
        }
    },
    {
        'enabled': True,
        'wire_1': 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
        'wire_2': 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
        'index': '3',
        'manhatten_distance': 135,
        'board_size': {
            'x': 123,
            'y': 182,
        },
        'central_port': {
            'x': 105,
            'y': 1,
        }
    },
    {
        'enabled': False,
        'wire_1': 'R997,D99,R514,D639,L438,D381,L251,U78,L442,D860,R271,U440,L428,U482,R526,U495,R361,D103,R610,D64,L978,U587,L426,D614,R497,D116,R252,U235,R275,D882,L480,D859,L598,D751,R588,D281,R118,U173,L619,D747,R994,U720,L182,U952,L49,D969,R34,D190,L974,U153,L821,U593,L571,U111,L134,U111,R128,D924,R189,U811,R100,D482,L708,D717,L844,U695,R277,D81,L107,U831,L77,U609,L629,D953,R491,D17,R160,U468,R519,D41,R625,D501,R106,D500,R473,D244,R471,U252,R440,U326,R710,D645,L190,D670,L624,D37,L46,D242,L513,D179,R192,D100,R637,U622,R322,U548,L192,D85,L319,D717,L254,D742,L756,D624,L291,D663,R994,U875,R237,U304,R40,D399,R407,D124,R157,D415,L405,U560,R607,U391,R409,U233,R305,U346,L233,U661,R213,D56,L558,U386,R830,D23,L75,D947,L511,D41,R927,U856,L229,D20,L717,D830,R584,U485,R536,U531,R946,U942,R207,D237,L762,U333,L979,U29,R635,D386,R267,D260,R484,U887,R568,D451,R149,U92,L379,D170,R135,U799,L617,D380,L872,U868,R48,U279,R817,U572,L728,D792,R833,U788,L940,D306,R230,D570,L137,U419,L429,D525,L730,U333,L76,D435,R885,U811,L937,D320,R152,U906,L461,U227,L118,U951,R912,D765,L638,U856,L193,D615,L347,U303,R317,U23,L139,U6,L525,U308,L624,U998,R753,D901,R556,U428,L224,U953,R804,D632,L764,U808,L487,U110,L593,D747,L659,D966,R988,U217,L657,U615,L425,D626,L194,D802,L440,U209,L28,U110,L564,D47,R698,D938,R13,U39,R703,D866,L422,D855,R535,D964,L813,D405,R116,U762,R974,U568,R934,U574,R462,D968,R331,U298,R994,U895,L204,D329,R982,D83,L301,D197,L36,U329,R144,U497,R300,D551,L74,U737,R591,U374,R815,U771,L681',
        'wire_2': 'L997,D154,R652,U379,L739,U698,R596,D862,L125,D181,R786,U114,R536,U936,L144,U936,R52,U899,R88,D263,R122,D987,L488,U303,R142,D556,L691,D769,L717,D445,R802,U294,L468,D13,R301,D651,L242,D767,R465,D360,L144,D236,R59,U815,R598,U375,R645,U905,L714,U440,R932,D160,L420,U361,L433,D485,L276,U458,R760,D895,R999,U263,R530,U691,L918,D790,L150,U574,R800,U163,R478,U112,L353,U30,L763,U239,L353,U619,R669,D822,R688,U484,L678,D88,R946,D371,L209,D175,R771,D85,R430,U16,R610,D326,R836,U638,L387,D996,L758,U237,L476,U572,L456,U579,L457,D277,L825,U204,R277,U267,L477,D573,L659,D163,L516,D783,R762,U146,L387,U700,R911,U335,L115,D887,R677,U312,R707,U463,L743,U358,L715,D603,R966,U21,L857,D680,R182,D977,L279,U196,R355,D624,L434,U410,R385,U47,L999,D542,L453,D735,R781,U115,R814,U110,R344,D139,R899,D650,L118,D774,L227,D140,L198,D478,R115,D863,R776,D935,R473,U722,R555,U528,L912,U268,R776,D223,L302,D878,R90,U52,L595,U898,L210,U886,R161,D794,L846,U404,R323,U616,R559,U510,R116,D740,L554,U231,R54,D328,L56,U750,R347,U376,L148,U454,L577,U61,L772,D862,R293,U82,L676,D508,L53,D860,L974,U733,R266,D323,L75,U218,L390,U757,L32,D455,R34,D363,L336,D67,R222,D977,L809,D909,L501,U483,L541,U923,R97,D437,L296,D941,L652,D144,L183,U369,L629,U535,L825,D26,R916,U131,R753,U383,L653,U631,R280,U500,L516,U959,R858,D830,R357,D87,R885,D389,L838,U550,R262,D529,R34,U20,L25,D553,L884,U806,L800,D988,R499,D360,R435,U381,R920,D691,R373,U714,L797,D677,L490,D976,L734,D585,L384,D352,R54,D23,R339,D439,L939,U104,L651,D927,L152',
        'index': '4',
        'manhatten_distance': 651,
        'board_size': {
            'x': 7700,
            'y': 7700,
        },
        'central_port': {
            'x': 27,
            'y': 42,
        }
    },
]


def process_wire_data(wire_data):
    circuit_array = []
    for x in range(0, wire_data['board_size']['x']):
        circuit_array.append([])
        for _ in range(0, wire_data['board_size']['y']):
            circuit_array[x].append(CHAR_BLANK)

    central_port = wire_data['central_port']
    circuit_array[central_port['x']][central_port['y']] = CHAR_CENTRAL_PORT

    draw_wire(wire_data['wire_1'], circuit_array,
              central_port, ignore_wire_crossing=True)
    draw_wire(wire_data['wire_2'], circuit_array, central_port)

    return circuit_array


def get_circuit_array_ascii(circuit_array):
    ascii_markup = ''
    for line in circuit_array:
        for port in line:
            if port == CHAR_CENTRAL_PORT:
                ascii_markup += f'<span class="central-port">{port}</span>'
            elif port == CHAR_CROSS:
                ascii_markup += f'<span class="intersection">{port}</span>'
            else:
                ascii_markup += port
        ascii_markup += '\n'
    return ascii_markup


def print_circuit_array(circuit_array):
    for line in circuit_array:
        for port in line:
            print(port, end='')
        print()


def draw_wire(wire, circuit_array, central_port, ignore_wire_crossing=False):
    instruction_vectors = parse_wire_instructions(wire)
    current_port = central_port.copy()
    previous_direction = None

    for instruction_vector in instruction_vectors:
        current_direction = instruction_vector['direction']
        PORT_CHAR = WIRE_H if instruction_vector['dx'] == 0 else WIRE_V
        x_start = current_port['x']
        y_start = current_port['y']
        x_end = x_start + instruction_vector['dx']
        y_end = y_start + instruction_vector['dy']
        current_port['x'] = x_end
        current_port['y'] = y_end

        draw_start_corner(circuit_array, x_start, y_start,
                          previous_direction, current_direction)

        range_step_x = 1 if x_start <= x_end else -1
        range_step_y = 1 if y_start <= y_end else -1
        range_start_x = x_start if range_step_x == 1 else x_start - 1
        range_stop_x = x_end + 1 if range_step_x == 1 else x_end - 1
        range_start_y = y_start if range_step_y == 1 else y_start - 1
        range_stop_y = y_end + 1 if range_step_y == 1 else y_end - 1

        for x in range(range_start_x, range_stop_x, range_step_x):
            for y in range(range_start_y, range_stop_y, range_step_y):
                if circuit_array[x][y] == WIRE_H or circuit_array[x][y] == WIRE_V:
                    if ignore_wire_crossing:
                        circuit_array[x][y] = PORT_CHAR
                    else:
                        circuit_array[x][y] = CHAR_CROSS
                elif circuit_array[x][y] == CHAR_BLANK:
                    circuit_array[x][y] = PORT_CHAR

        previous_direction = current_direction


def count_steps(wire, circuit_array, central_port):
    steps = []
    instruction_vectors = parse_wire_instructions(wire)
    current_port = central_port.copy()
    current_steps = 0

    last_was_corner = False
    for instruction_vector in instruction_vectors:
        x_start = current_port['x']
        y_start = current_port['y']
        x_end = x_start + instruction_vector['dx']
        y_end = y_start + instruction_vector['dy']
        current_port['x'] = x_end
        current_port['y'] = y_end

        # counting is off. range forwards counts from the first char
        # range backwards counts from the second char.
        range_step_x = 1 if x_start <= x_end else -1
        range_step_y = 1 if y_start <= y_end else -1
        range_start_x = x_start if range_step_x == 1 else x_start
        range_stop_x = x_end + 1 if range_step_x == 1 else x_end - 1
        range_start_y = y_start if range_step_y == 1 else y_start
        range_stop_y = y_end + 1 if range_step_y == 1 else y_end - 1

        for x in range(range_start_x, range_stop_x, range_step_x):
            for y in range(range_start_y, range_stop_y, range_step_y):
                if circuit_array[x][y] == CHAR_CENTRAL_PORT:
                    continue
                # Avoid counting corners twice.
                if last_was_corner and circuit_array[x][y] in CORNER_CHARS:
                    last_was_corner = False
                    continue

                # print(circuit_array[x][y])
                current_steps += 1

                if circuit_array[x][y] in CORNER_CHARS:
                    last_was_corner = True
                elif circuit_array[x][y] == CHAR_CROSS:
                    steps.append({
                        'steps': current_steps,
                        'x': x,
                        'y': y,
                    })

    return steps


def draw_start_corner(circuit_array, x_start, y_start, previous_direction, current_direction):
    if circuit_array[x_start][y_start] in WIRE_CHARS:
        if previous_direction == 'R' and current_direction == 'U':
            circuit_array[x_start][y_start] = WIRE_UL
        elif previous_direction == 'R' and current_direction == 'D':
            circuit_array[x_start][y_start] = WIRE_DL
        elif previous_direction == 'L' and current_direction == 'U':
            circuit_array[x_start][y_start] = WIRE_UR
        elif previous_direction == 'L' and current_direction == 'D':
            circuit_array[x_start][y_start] = WIRE_DR
        elif previous_direction == 'U' and current_direction == 'R':
            circuit_array[x_start][y_start] = WIRE_DR
        elif previous_direction == 'U' and current_direction == 'L':
            circuit_array[x_start][y_start] = WIRE_DL
        elif previous_direction == 'D' and current_direction == 'R':
            circuit_array[x_start][y_start] = WIRE_UR
        elif previous_direction == 'D' and current_direction == 'L':
            circuit_array[x_start][y_start] = WIRE_UL


def calc_manhatten_distance(central_port, circuit_array):
    distances = []
    for x in range(0, len(circuit_array)):
        line = circuit_array[x]
        for y in range(0, len(line)):
            port = line[y]
            if port == CHAR_CROSS:
                dx = abs(central_port['x'] - x)
                dy = abs(central_port['y'] - y)
                distances.append(dx + dy)

    smallest_distance = math.inf
    for distance in distances:
        if distance < smallest_distance:
            smallest_distance = distance

    return smallest_distance


def parse_wire_instructions(wire):
    instruction_vectors = []

    for instruction in wire.split(','):
        direction = instruction[0]
        distance = int(instruction[1:])

        instruction_vector = {
            'dx': 0,
            'dy': 0,
            'direction': direction
        }

        if direction == 'R':
            instruction_vector['dy'] = distance
        elif direction == 'L':
            instruction_vector['dy'] = -distance
        elif direction == 'U':
            instruction_vector['dx'] = -distance
        elif direction == 'D':
            instruction_vector['dx'] = distance

        instruction_vectors.append(instruction_vector)

    return instruction_vectors


def write_to_file(content):
    import os
    dir_path = os.path.dirname(os.path.realpath(
        __file__)) + f'/{OUTPUT_FILE_NAME}'
    with open(dir_path, 'w') as file:
        file.write(content)
        file.close()


def main():
    file_content = OUTPUT_FILE_PREFIX

    for wire_data in wires:
        if wire_data['enabled'] == False:
            continue

        circuit_array = process_wire_data(wire_data)

        # Prevent printing the forth circuit as it’s way too big.
        if wire_data['index'] != '4':
            print()
            print_circuit_array(circuit_array)

            circuit_ascii = get_circuit_array_ascii(circuit_array)

            file_content += f"""
            <h2>Input {wire_data["index"]}</h2>
            <pre class="input-{wire_data["index"]}">{circuit_ascii}</pre>
            """.strip()

        manhatten_distance = calc_manhatten_distance(
            wire_data['central_port'], circuit_array)

        assert manhatten_distance == wire_data['manhatten_distance']

    write_to_file(file_content)


if __name__ == '__main__':
    main()
