import bs4
from bs4 import BeautifulSoup
import requests
from data.Country import Country

WIKI_STATES_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
WIKI_NEIGHBOURS_URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders'
WIKI_HOME = 'https://en.wikipedia.org'


def table_country_links(a: bs4.Tag) -> bool:
    """Get the a tags with the country links only."""
    tags = ['b', 'td', 'tr', 'tbody', 'table']
    try:
        if a.name != 'a':
            return False
        for i in range(5):
            a = a.parent
            if a.name != tags[i]:
                return False
    except AttributeError:
        return False
    return True


def table_country_rows(tr: bs4.Tag) -> bool:
    """Get the table rows for each country and its neighbours."""
    tags = ['tbody', 'table']
    try:
        if tr.name != 'tr':
            return False
        for i in range(2):
            tr = tr.parent
            if tr.name != tags[i]:
                return False
    except AttributeError:
        return False
    return True


def get_country_links() -> list[str]:
    """Get the links to each country's Wikipedia page."""
    r = requests.get(WIKI_STATES_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_elements = soup.find_all(table_country_links)
    links = []
    for elem in country_elements:
        links.append(elem.get('href'))
    return links


def get_country_name(link: str) -> str:
    """Take the name of the country from its page. Names differ from the countries page and the neighbours page. We
    will therefore take the name from the country's page
    """
    r = requests.get(WIKI_HOME + link)
    soup = BeautifulSoup(r.text, features='lxml')
    return soup.body.h1.text


def get_country_neighbours(link: str):
    r = requests.get(WIKI_NEIGHBOURS_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_rows = soup.find_all(table_country_rows)


if __name__ == '__main__':
    country_links = get_country_links()
    for country_link in country_links:
        Country.create(name=get_country_name(country_link), wiki_link=country_link)
