#!/usr/bin/env python3

from typing import List, Dict

test_orbit_data = [
    'COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN'
]


def read_orbit_data() -> List[str]:
    """
    Reads a text file called “orbit-data.txt”
    and returns a list of strings representing direct orbit relationships.
    """
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '/orbit-data.txt'
    orbit_data = ''

    with open(dir_path, 'r') as file:
        orbit_data = file.read()
        file.close()

    return orbit_data.strip().split('\n')


def build_orbit_map(orbit_data):
    """
    Constructs a map of orbit paths for all known objects in a system.

    For example, given `test_orbit_data` as an input,
    the object “G” has an orbit path of “COM)B)G” and
    the object “H” has an orbit path of “COM)B)G)H”.
    """
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


def find_shortest_route_length(orbit_data, object_1, object_2):
    orbit_map = build_orbit_map(orbit_data)
    path_1 = orbit_map[object_1]
    path_2 = orbit_map[object_2]

    common_object = find_common_object(path_1, path_2)

    path_segment_1 = path_1[:path_1.index(common_object) - 1]
    path_segment_2 = path_2[:path_2.index(common_object) - 1]
    length_path_segment_1 = len(path_segment_1.split(')'))
    length_path_segment_2 = len(path_segment_2.split(')'))
    return length_path_segment_1 + length_path_segment_2


def find_common_object(orbit_path_1, orbit_path_2):
    """
    Searches two orbit paths for a common object and returns it.
    """
    for system_a in orbit_path_1.split(')'):
        for system_b in orbit_path_2.split(')'):
            if system_a == system_b:
                return system_a


def main():
    orbit_data = read_orbit_data()
    # orbit_data = test_orbit_data
    shortest_route_length = find_shortest_route_length(
        orbit_data, 'SAN', 'YOU')
    print(shortest_route_length)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
