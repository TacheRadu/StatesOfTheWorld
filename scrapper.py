from time import sleep
from types import Union
from typing import Optional, Any

import requests

from tools.get_country_info import *

WIKI_HOME = 'https://en.wikipedia.org'


@db_session
def get_country(link: str) -> Union[Optional[Country], Any]:
    """
    The main function that gets the country data.
    Get the soup for the country wiki page, then pass it to different functions that get different things

    :param link: relative link to the country's wikipedia page
    :return: The country, after extracting data from the page
    :rtype: Country
    """
    for i in range(5):
        try:
            r = requests.get(WIKI_HOME + link)
        except requests.RequestException:
            print('Request went bad..')
            sleep(0.2)
            continue
        break

    if r.status_code != 200:
        print('Didn\'t receive what I expected..')
        return
    try:
        soup = BeautifulSoup(r.text, features='lxml')
    except Exception:
        print('Data in response is not relevant')
        return

    country = Country.get(wiki_link=link)
    if country is None:
        country = Country(wiki_link=link)
    country.name = get_country_name(soup)
    print(country.name)
    country_table = soup.find('table', {'class': 'infobox ib-country vcard'})
    country.capitals = get_country_capitals(country_table)
    country.population = get_country_population(country_table)
    country.density = get_country_density(country_table)
    country.surface = get_country_area(country_table)
    country.area = get_country_area(country_table)
    country.language_categories = get_country_language_categories(country_table)
    country.time_zone = get_country_time_zone(country_table)
    country.government = get_country_government(country_table)
    country.driving_side = get_country_driving_side(country_table)
    return country


def main():
    """
    We run things from here, duuh.
    :return: None
    """
    country_links = get_country_links()
    for country_link in country_links:
        get_country(country_link)
    for country_link in country_links:
        print(country_link)
        get_country_neighbours(country_link)


if __name__ == '__main__':
    main()
