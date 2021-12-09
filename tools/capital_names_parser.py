import bs4
import re
from tools.hlp import strip_citations


def parse_capital_text(item: bs4.Tag) -> str:
    """Parses the particular item in which a capital name is, extracts and returns it.
    It takes up the text up to the first br tag, since from that point forward the text represents coordinates of the
    cities.
    From the resulting string, remove the citations, which are between square brackets. Since they are all one after
    the other and they are the only things within square brackets, we can just remove everything between an open and
    a closed bracket.
    """
    capital = ''
    for elem in item.find_all():
        if elem.name == 'br':
            break
        capital += elem.text
    capital = strip_citations(capital)
    return capital
