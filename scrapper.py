from tools.get_country_info import *

WIKI_HOME = 'https://en.wikipedia.org'


@db_session
def get_country(link: str) -> Country:
    """The main function that gets the country data.
    Get the soup for the country wiki page, then pass it to different functions that get different things
    """
    r = requests.get(WIKI_HOME + link)
    soup = BeautifulSoup(r.text, features='lxml')
    country = Country.get(wiki_link=link)
    if country is None:
        country = Country(wiki_link=link)
    country.name = get_country_name(soup)
    print(country.name)
    country_table = soup.find('table', {'class': 'infobox ib-country vcard'})
    country.capitals = get_country_capitals(country_table)
    country.language_categories = get_country_language_categories(country_table)
    return country


def main():
    country_links = get_country_links()
    for country_link in country_links:
        get_country(country_link)
    print("Now getting neighbours")
    # for country_link in country_links:
    #     get_country_neighbours(country_link)


if __name__ == '__main__':
    main()
