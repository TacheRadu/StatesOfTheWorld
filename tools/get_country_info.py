from pony.orm import db_session
from bs4 import BeautifulSoup

from data.capital import Capital
from data.language import Language
from data.language_category import LanguageCategory
from tools.html_filters import *
from data.country import Country
from tools.hlp import beautiful_strip, to_int, to_float
from tools.parser import parse_capital_text, parse_languages_text, split_by_tags
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


def get_country_capitals(table: bs4.Tag) -> list[Capital]:
    """Get a list of capitals. A country might have no capital, one or more capitals. So search for a table head
    which contains the word Capital. If the country has capitals, that will exist. If we can't find it, it doesn't
    have capitals, so we're returning an empty list. Beneath the table head will be the table data with the capitals.
    If there is an unordered list inside, then we have multiple capitals. Otherwise, the table data has only one
    capital.
    We parse the page elements and get the capital name.
    """
    capital_header = table.find(lambda tag: tag.name == 'th' and 'Capital' in tag.text)
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
                    capitals.append(capital)
                return capitals

            capital_name = parse_capital_text(td)
            capital = Capital.get(name=capital_name)
            if capital is None:
                capital = Capital(name=capital_name)
            return [capital]
    return []


def get_country_language_categories(table: bs4.Tag) -> list[LanguageCategory]:
    language_headers = table.find_all(lambda tag: tag.name == 'th' and 'language' in tag.text
                                      and not tag.find('div', {'class': 'ib-country-names'}))
    categories = []
    for language_header in language_headers:
        category = beautiful_strip(''.join(language_header.strings))
        language_category = LanguageCategory.get(category=category)
        if not language_category:
            language_category = LanguageCategory(category=category)
        td = language_header.find_next_sibling('td')
        language_category.languages = get_category_languages(td)
        categories.append(language_category)
    return categories


def get_category_languages(td: bs4.Tag) -> list[Language]:
    if td:
        ul = td.find('ul')
        if ul:
            # East Timor case where there is a list in a list for no reason
            if ul.find('ul'):
                ul = ul.find('ul')
            languages = []
            for li in ul.find_all('li'):
                potential_languages = parse_languages_text(li)
                potential_languages = list(
                    map(
                        lambda l: Language(language=l) if not Language.get(language=l) else Language.get(language=l),
                        potential_languages
                    )
                )
                languages.extend(potential_languages)
            return languages

        languages = parse_languages_text(td)
        languages = list(
            map(
                lambda l: Language(language=l) if not Language.get(language=l) else Language.get(language=l), languages
            )
        )
        return languages
    return []


def get_country_population(table: bs4.Tag) -> int:
    th = table.find(lambda table_h: table_h.name == 'th' and 'Population' in table_h.text)
    td = th.parent.next_sibling.td
    return to_int(beautiful_strip(td.text))


def get_country_density(table: bs4.Tag) -> float:
    th = table.find(lambda table_h: table_h.name == 'th' and 'Density' in table_h.text)
    if th:
        td = th.find_next_sibling('td')
        return to_float(beautiful_strip(td.text))
    return 0


def get_country_area(table: bs4.Tag) -> float:
    th = table.find(lambda table_h: table_h.name == 'th' and 'Area' in table_h.text)
    if th:
        tds = []
        for tr in th.parent.find_next_siblings('tr'):
            tds.append(tr.td)
            if 'mergedbottomrow' in tr.get('class'):
                break
        area = 0
        for td in tds:
            area += to_float(beautiful_strip(td.text))
        return area
    return 0


def get_country_time_zone(table: bs4.Tag) -> str:
    th = table.find(lambda table_h: table_h.name == 'th' and 'Time zone' in table_h.text)
    if th:
        tds = [th.find_next_sibling('td')]
        for tr in th.parent.find_next_siblings('tr'):
            if not tr.get('class'):
                break
            tds.append(tr.td)
            if 'mergedbottomrow' in tr.get('class'):
                break
        time_zone = ''
        for td in tds:
            strings = split_by_tags(td, ['br', 'span'])
            if len(strings) == 1 and not td.text.startswith('Note:'):
                time_zone += beautiful_strip(td.text) + '\n'
            else:
                for string in strings:
                    # Case for France:
                    if string.startswith('Note:'):
                        break
                    time_zone += beautiful_strip(string) + '\n'
        print(time_zone)
        return time_zone
    return ''


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
