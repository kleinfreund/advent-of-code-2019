#!/usr/bin/env python3

from typing import List
import math
import textwrap

COLOR_BLACK = '0'
COLOR_WHITE = '1'
COLOR_TRANSPARENT = '2'


def read_image_data(filename) -> str:
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/' + filename
    image_data = ''

    with open(dir_path, 'r') as file:
        image_data = file.read()
        file.close()

    return image_data.strip()


def wrap_into_layers(image_data: str, width: int, height: int) -> List[List[str]]:
    layers = []

    flat_layers = textwrap.wrap(image_data, width * height)
    for layer in flat_layers:
        layers.append(textwrap.wrap(layer, 25))

    return layers


def render_image(layers: List[List[str]], width: int, height: int) -> List[List[str]]:
    image = [['#' for pixel in range(width)] for line in range(height)]
    for layer in list(reversed(layers)):
        for x, line in enumerate(layer):
            for y, pixel in enumerate(line):
                if pixel == COLOR_TRANSPARENT:
                    continue
                elif pixel == COLOR_BLACK:
                    image[x][y] = ' '
                elif pixel == COLOR_WHITE:
                    image[x][y] = '◼'

    return image


def print_image(image: List[List[str]]):
    for line in image:
        print(''.join(line))


def main():
    image_data = read_image_data('image-data.txt')
    layers = wrap_into_layers(image_data, 25, 6)
    image = render_image(layers, 25, 6)
    print_image(image)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
