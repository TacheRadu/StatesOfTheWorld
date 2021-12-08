import bs4


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
        if tr.name != 'tr' or len(tr.find_all('td')) != 6:
            return False
        for i in range(2):
            tr = tr.parent
            if tr.name != tags[i]:
                return False
    except AttributeError:
        return False
    return True


