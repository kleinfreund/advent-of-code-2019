#!/usr/bin/env python3

# from typing import List
import math
import textwrap


def read_image_data() -> str:
    import os
    dir_path = os.path.dirname(os.path.realpath(
        __file__)) + '/image-data.txt'
    image_data = ''

    with open(dir_path, 'r') as file:
        image_data = file.read()
        file.close()

    return image_data.strip()


def get_layers(image_data, width, height):
    return textwrap.wrap(image_data, width * height)


def find_corruption_data(layers):
    target_layer = None
    instances_of_0 = math.inf

    for layer in layers:
        zeroes = len(find_instances(layer, '0'))

        if zeroes < instances_of_0:
            instances_of_0 = zeroes
            target_layer = layer

    instances_of_1 = len(find_instances(target_layer, '1'))
    instances_of_2 = len(find_instances(target_layer, '2'))

    return instances_of_1 * instances_of_2


def find_instances(string, search_char):
    return [i for i, char in enumerate(string) if char == search_char]


def main():
    image_data = read_image_data()
    layers = get_layers(image_data, 25, 6)
    result = find_corruption_data(layers)
    print(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
