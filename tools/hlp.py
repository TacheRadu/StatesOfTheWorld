import math
import re

import bs4


def beautiful_strip(string: str) -> str:
    return re.sub('\n\n\n.*', '', strip_citations(string))


def strip_citations(string: str) -> str:
    return re.sub(' +', ' ', re.sub('\[(.)*]', '', string).replace('languageand', 'language and')
                  .replace('languagesand', 'languages and'))


def get_number_and_decimals(string: str, delimiters: list[str]) -> tuple[int, int]:
    number_chars = []
    numbers_after_last_delimiter = 0
    increment_factor = 0
    for c in string.strip():
        if not c.isdigit() and c not in delimiters:
            break
        if c not in delimiters:
            number_chars.append(c)
            numbers_after_last_delimiter += increment_factor
        elif c == delimiters[-1]:
            numbers_after_last_delimiter = 0
            increment_factor = 1
    try:
        return int(''.join(number_chars)), numbers_after_last_delimiter
    except ValueError:
        return 0, 0


def to_int(string: str) -> int:
    multiplication_factor = 0
    division_factor = 0
    if 'million' in string:
        multiplication_factor = 6
        number, division_factor = get_number_and_decimals(string.strip(), ['.'])
    elif 'billion' in string:
        multiplication_factor = 9
        number, division_factor = get_number_and_decimals(string.strip(), ['.'])
    else:
        number, _ = get_number_and_decimals(string.strip(), [','])
    return number * int(math.pow(10, multiplication_factor - division_factor))


def to_float(string: str) -> float:
    number, div = get_number_and_decimals(string.strip(), [',', '.'])
    return number / math.pow(10, div)
