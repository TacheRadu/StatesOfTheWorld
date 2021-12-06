import bs4
from bs4 import BeautifulSoup
import requests

WIKI_STATES_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'


def check_right_structure(a: bs4.PageElement):
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


if __name__ == '__main__':
    r = requests.get(WIKI_STATES_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    countries = dict()
    country_elements = soup.find_all(check_right_structure)
    for elem in country_elements:
        countries[elem.text] = elem.get('href')
    print(countries)
