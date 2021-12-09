import re

from pony.orm import db_session
from bs4 import BeautifulSoup

from data.capital import Capital
from data.language import Language
from data.language_category import LanguageCategory
from tools.html_filters import *
from data.country import Country
from tools.hlp import strip_citations
from tools.capital_names_parser import parse_capital_text
import requests

WIKI_STATES_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
WIKI_NEIGHBOURS_URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders'


def get_country_links() -> list[str]:
    """Get the links to each country's Wikipedia page."""
    r = requests.get(WIKI_STATES_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_elements = soup.find_all(table_country_links)
    links = []
    for elem in country_elements:
        links.append(elem.get('href'))
    return links


def get_country_name(soup: bs4.BeautifulSoup) -> str:
    """Take the name of the country from its page. Names differ from the countries page and the neighbours page. We
    will therefore take the name from the country's page
    The name is in the body, in the first h1 tag, and we take the tag's text.
    """
    return soup.body.h1.text


def get_country_capitals(soup: bs4.BeautifulSoup) -> list[Capital]:
    """Get a list of capitals. A country might have no capital, one or more capitals. So search for a table head
    which contains the word Capital. If the country has capitals, that will exist. If we can't find it, it doesn't
    have capitals, so we're returning an empty list. Beneath the table head will be the table data with the capitals.
    If there is an unordered list inside, then we have multiple capitals. Otherwise, the table data has only one
    capital.
    We parse the page elements and get the capital name.
    """
    capital_header = soup.find(lambda tag: tag.name == 'th' and 'Capital' in tag.text)
    if capital_header:
        td = capital_header.find_next_sibling('td')
        if td:

            # Special Switzerland case, which has no official capital, but a de facto one.
            # I'll try to make it a bit more general, though
            ul = td.find('ul')
            if ul:
                capitals = []
                for elem in ul.find_all('li'):
                    capital_name = parse_capital_text(elem)
                    capital = Capital.get(name=capital_name)
                    if capital is None:
                        capital = Capital(name=capital_name)
                    print('   ', capital)
                    capitals.append(capital)
                return capitals

            capital_name = parse_capital_text(td)
            capital = Capital.get(name=capital_name)
            if capital is None:
                capital = Capital(name=capital_name)
            print('   ', capital)
            return [capital]
    return []


def get_country_language_categories(soup: bs4.BeautifulSoup) -> list[LanguageCategory]:
    language_headers = soup.find_all(lambda tag: tag.name == 'th' and 'language' in tag.text
                                     and not tag.find('div', {'class': 'ib-country-names'}))
    cats = []
    for language_header in language_headers:
        category = strip_citations(''.join(language_header.strings))
        print('   ' * 2, category)
        language_cat = LanguageCategory.get(category=category)
        if not language_cat:
            language_cat = LanguageCategory(category=category)
        td = language_header.find_next_sibling('td')
        language_cat.languages = get_category_languages(td)
        cats.append(language_cat)
    return cats


def get_category_languages(td: bs4.BeautifulSoup) -> list[Language]:
    if td:
        ul = td.find('ul')
        if ul:
            # East Timor case where there is a list in a list for no reason
            if ul.find('ul'):
                ul = ul.find('ul')
            languages = []
            for li in ul.find_all('li'):
                language_name = re.sub('\n\n\n.*', '', strip_citations(''.join(li.strings)))
                if language_name == '':
                    continue
                language = Language.get(language=language_name)
                if not language:
                    language = Language(language=language_name)
                print('   ' * 3, language)
                languages.append(language)
            return languages
        language_name = re.sub('\n\n\n.*', '', strip_citations(''.join(td.strings)))
        language = Language.get(language=language_name)
        if not language:
            language = Language(language=language_name)
        print('   ' * 3, language)
        return [language]
    return []


@db_session
def get_country_neighbours(link: str) -> None:
    """Takes the path to the wikipedia page of the country we compute the neighbours of, starting from what's after
    .org. The function will look in the table on the page, find the row for the specified country and looks for the
    countries corresponding to it, looking them up by their link."""
    r = requests.get(WIKI_NEIGHBOURS_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_rows = soup.find_all(table_country_rows)
    my_country_rows = [x for x in country_rows if x.find('td').find('a').get('href') == link]
    if link == '/wiki/Danish_Realm':
        my_country_row = [x for x in country_rows if x.find('td').find('a').get('href') == '/wiki/Denmark'][0]
    elif len(my_country_rows) == 0:
        return
    else:
        my_country_row = my_country_rows[0]
    neighbours = []
    for x in my_country_row.find_all('td')[-1].find_all('a'):
        if not x.get('href').startswith('#cite_note'):
            neighbouring_country = Country.get(wiki_link=x.get('href').replace('/wiki/Denmark', '/wiki/Danish_Realm'))
            if neighbouring_country is not None:
                neighbours.append(neighbouring_country)
    country = Country.get(wiki_link=link)
    country.neighbours = neighbours
