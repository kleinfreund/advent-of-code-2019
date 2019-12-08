#!/usr/bin/env python3


def is_valid_password(number):
    """
    Determines if a password is valid.
    https://adventofcode.com/2019/day/4#part2

    >>> is_valid_password(123454)
    False
    >>> is_valid_password(166677)
    True
    >>> is_valid_password(166788)
    True
    >>> is_valid_password(156888)
    False
    """
    str_representation = str(number)

    has_decreasing_value = False
    current_value = 0
    for str_digit in list(str_representation):
        if int(str_digit) < current_value:
            has_decreasing_value = True
            break

        current_value = int(str_digit)

    if has_decreasing_value:
        return False

    found_double_digits = []
    for double_digit in [x*11 for x in range(1, 10)]:
        if str(double_digit) in str_representation:
            found_double_digits.append(double_digit)

    if len(found_double_digits) == 0:
        # If there is no double-digit instance at all, the password is disqualified.
        return False
    else:
        # If there is a double-digit instance, but it’s part of a larger group of multiple digits,
        # the password is also disqualified:
        # 222345 is not valid; however, 222445 is
        # because it has a double-digit pair (44) that is not part of a larger group.
        # tricky: 166677
        valid_double_digits = found_double_digits.copy()
        for found_double_digit in found_double_digits:
            str_double_digit = str(found_double_digit)
            double_digit_pos = str_representation.find(str_double_digit)
            if str_double_digit in str_representation[double_digit_pos + 1:]:
                valid_double_digits.remove(found_double_digit)

        if len(valid_double_digits) == 0:
            return False

    return True


def get_number_of_valid_passwords(lower_bound, upper_bound):
    """
    >>> get_number_of_valid_passwords(158126, 624574 + 1)
    1131
    """
    valid_passwords = []

    for password in range(lower_bound, upper_bound):
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
