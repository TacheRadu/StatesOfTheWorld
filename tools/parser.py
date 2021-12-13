import re

import bs4
from tools.hlp import beautiful_strip, strip_citations


def parse_capital_text(item: bs4.Tag) -> str:
    """Parses the particular item in which a capital name is, extracts and returns it.
    It takes up the text up to the first br tag, since from that point forward the text represents coordinates of the
    cities.
    From the resulting string, remove the citations, which are between square brackets. Since they are all one after
    the other and they are the only things within square brackets, we can just remove everything between an open and
    a closed bracket.
    """
    capital = ''
    for elem in item.descendants:
        if elem.name == 'br':
            break
        if isinstance(elem, bs4.NavigableString):
            capital += elem
    capital = strip_citations(capital)
    return capital


def split_by_tags(item: bs4.Tag, tags: list[str]) -> list[str]:
    strings = []
    string = ''
    for elem in item.descendants:
        if elem.name in tags:
            string = beautiful_strip(string)
            if string != '':
                strings.append(string)
            string = ''
        else:
            if isinstance(elem, bs4.NavigableString):
                string += elem
    string = beautiful_strip(string)
    if string != '':
        strings.append(string)
    return strings


def parse_languages_text(item: bs4.Tag) -> list[str]:

    # For the incredible cases of Pakistan and the countries with languages split by commas:
    languages = re.split(',|\u2022', beautiful_strip(item.text))
    if len(languages) > 1:
        languages = [beautiful_strip(language) for language in languages if beautiful_strip(language) != '']
        # Amazing case for Luxembourg:

        return ['Luxembourgish' if language.find('Luxembourgish') != -1 else language for language in languages]

    return split_by_tags(item, ['br', 'small'])
