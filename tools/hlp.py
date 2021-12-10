import re


def beautiful_strip(string: str) -> str:
    return re.sub('\n\n\n.*', '', strip_citations(string))


def strip_citations(string: str) -> str:
    return re.sub(' +', ' ', re.sub('\[(.)*]', '', string).replace('languageand', 'language and')
                  .replace('languagesand', 'languages and'))
