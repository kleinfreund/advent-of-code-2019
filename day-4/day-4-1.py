#!/usr/bin/env python3


def is_valid_password(number):
    """
    Determines if a password is valid.
    https://adventofcode.com/2019/day/4

    >>> is_valid_password(123454)
    False
    >>> is_valid_password(166677)
    True
    >>> is_valid_password(166788)
    True
    >>> is_valid_password(156888)
    True
    """
    str_representation = str(number)
    has_double_digit = False
    for double_digit in [x*11 for x in range(1, 10)]:
        if str(double_digit) in str_representation:
            has_double_digit = True
            break

    if not has_double_digit:
        return False

    has_decreasing_value = False
    current_value = 0
    for str_digit in list(str_representation):
        if current_value > int(str_digit):
            has_decreasing_value = True
            break

        current_value = int(str_digit)

    if has_decreasing_value:
        return False

    return True


def get_number_of_valid_passwords(lower_bound, upper_bound):
    """
    >>> get_number_of_valid_passwords(158126, 624574 + 1)
    1665
    """
    valid_passwords = []
    for password in range(158126, 624574 + 1):
        if is_valid_password(password):
            valid_passwords.append(password)

    return len(valid_passwords)


def main():
    number_of_valid_passwords = get_number_of_valid_passwords(
        158126, 624574 + 1)
    print(number_of_valid_passwords)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
