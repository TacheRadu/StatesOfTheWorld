import math
import re


def beautiful_strip(string: str) -> str:
    """
    Remove unnecessary data from string
    :param string: string to be formatted
    :return: formatted string
    :rtype: str
    """
    return re.sub('\n\n\n.*', '', strip_citations(string))


def strip_citations(string: str) -> str:
    """
    Strip a string of citations, too many spaces, and replace 'languageand' with 'languages and'
    :param string: string to be stripped
    :return: stripped string
    :rtype: str
    """
    return re.sub(' +', ' ', re.sub('\[(.)*?]', '', string).replace('languageand', 'language and')
                  .replace('languagesand', 'languages and'))


def get_number_and_decimals(string: str, delimiters: list[str]) -> tuple[int, int]:
    """
    Parse a string and get its corresponding number, in the form of two values: the number as an int with the delimiters
    removed and another int representing the number of decimals
    :param string: string to parse
    :param delimiters: list of string delimiters. If any character other than these or a digit is found, parsing stops.
    The last delimiter should be the one representing the decimals delimiter. It will be used to compute the number of
    decimals
    :return: tuple with the number without decimal point and the number of decimals (e.g. for '123.23' it will return
    (12323, 2)
    :rtype: tuple[int, int]
    """
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
    """
    Turn a string containing a number following 'million' or 'billion' into its integer equivalent
    :param string: The string to parse
    :return: The converted integer
    :rtype: int
    """
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
    """
    Turns a string into its float equivalent
    :param string: String to be parsed
    :return: The converted float
    :rtype: float
    """
    number, div = get_number_and_decimals(string.strip(), [',', '.'])
    return number / math.pow(10, div)
