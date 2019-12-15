#!/usr/bin/env python3

from typing import List, Dict

"""
L: COM)B)C)D)E)J)K 7
K: COM)B)C)D)E)J   6
J: COM)B)C)D)E     5
E: COM)B)C)D       4
D: COM)B)C         3
C: COM)B           2
B: COM             1

F: COM)B)C)D)E     5
  [E: COM)B)C)D       4] → these don’t count again
  [D: COM)B)C         3] → these don’t count again
  [C: COM)B           2] → these don’t count again

I: COM)B)C)D       4
  [D: COM)B)C         3] → these don’t count again
  [C: COM)B           2] → these don’t count again

H: COM)B)G         3
G: COM)B           2
"""

test_orbit_data = [
    'COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'
]


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


def read_orbit_data(filename) -> List[int]:
    return read_file(filename).split('\n')


def build_orbit_map(orbit_data):
    orbit_map = {}
    for orbit in orbit_data:
        [_, orbiter] = orbit.split(')')
        if orbiter not in orbit_map:
            orbit_map[orbiter] = ''

    for leave_orbit in orbit_map.keys():
        fill_in_orbit_map(orbit_data, orbit_map, leave_orbit, leave_orbit)

    return orbit_map


def fill_in_orbit_map(orbit_data, orbit_map, leave_orbit, current_orbiter):
    next_orbiter = None
    for orbit in orbit_data:
        [host, orbiter] = orbit.split(')')

        if orbiter == current_orbiter:
            orbit_map[leave_orbit] += ')' + host
            next_orbiter = host
            break

    if next_orbiter and next_orbiter != leave_orbit:
        fill_in_orbit_map(orbit_data, orbit_map, leave_orbit, next_orbiter)
    else:
        orbit_map[leave_orbit] = orbit_map[leave_orbit][1:]


def get_total_orbit_count(orbit_data):
    """
    >>> get_total_orbit_count(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L'])
    42
    """
    orbit_map = build_orbit_map(orbit_data)

    total = 0
    for path in orbit_map.values():
        total += len(path.split(')'))

    return total


def main():
    orbit_data = read_orbit_data('orbit-data.txt')
    # orbit_data = test_orbit_data
    total_orbit_count = get_total_orbit_count(orbit_data)
    print(total_orbit_count)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
