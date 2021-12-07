import bs4
from bs4 import BeautifulSoup
import requests
from data.Country import Country

WIKI_STATES_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
WIKI_NEIGHBOURS_URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders'


def in_table_of_countries(a: bs4.PageElement):
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


def get_country_links():
    r = requests.get(WIKI_STATES_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_elements = soup.find_all(in_table_of_countries)
    countries = []
    for elem in country_elements:
        countries.append((Country(name=elem.text), elem.get('href')))
    return countries


def get_country_neighbours():
    r = requests.get(WIKI_NEIGHBOURS_URL)
    soup = BeautifulSoup(r.text, features='lxml')


if __name__ == '__main__':
    links = get_country_links()