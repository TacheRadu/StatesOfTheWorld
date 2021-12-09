import re


def strip_citations(string: str) -> str:
    return re.sub(' +', ' ', re.sub('\[(.)*]', '', string).replace('languageand', 'language and')
                  .replace('languagesand', 'languages and'))
