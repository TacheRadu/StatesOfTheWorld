from bs4 import BeautifulSoup
import requests
from data.Country import Country
from tools.html_filters import *

WIKI_STATES_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
WIKI_NEIGHBOURS_URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders'
WIKI_HOME = 'https://en.wikipedia.org'


def get_country_links() -> list[str]:
    """Get the links to each country's Wikipedia page."""
    r = requests.get(WIKI_STATES_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_elements = soup.find_all(table_country_links)
    links = []
    for elem in country_elements:
        links.append(elem.get('href'))
    return links


def get_country(link: str) -> Country:
    """The main function that gets the country data.
    Get the soup for the country wiki page, then pass it to different functions that get different things
    """
    r = requests.get(WIKI_HOME + link)
    soup = BeautifulSoup(r.text, features='lxml')
    country = Country.get_or_create(wiki_link=link)[0]
    country.name = get_country_name(soup)
    country.save()
    return country


def get_country_name(soup: bs4.BeautifulSoup) -> str:
    """Take the name of the country from its page. Names differ from the countries page and the neighbours page. We
    will therefore take the name from the country's page
    The name is in the body, in the first h1 tag, and we take the tag's text.
    """
    return soup.body.h1.text


def get_country_neighbours(link: str) -> list[Country]:
    r = requests.get(WIKI_NEIGHBOURS_URL)
    soup = BeautifulSoup(r.text, features='lxml')
    country_rows = soup.find_all(table_country_rows)
    my_country_rows = [x for x in country_rows if x.find('td').find('a').get('href') == link]
    if link == '/wiki/Danish_Realm':
        my_country_row = [x for x in country_rows if x.find('td').find('a').get('href') == '/wiki/Denmark'][0]
    elif len(my_country_rows) == 0:
        return []
    else:
        my_country_row = my_country_rows[0]
    return [Country.get_or_create(wiki_link=x.get('href'))[0] for x in my_country_row.find_all('td')[-1].find_all('a')
            if not x.get('href').startswith('#cite_note')]


if __name__ == '__main__':
    country_links = get_country_links()
    my_country = Country.select(Country).where(Country.name == 'Romania')[0]
    for neigh in my_country.get_neighbours():
        print(neigh)
    #for country_link in country_links:
    #    my_country = get_country(country_link)
    #    print(my_country)
    #    my_country.neighbours = get_country_neighbours(my_country.wiki_link)
    #    my_country.save_neighbours()
