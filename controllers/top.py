import json
from data.country import Country
from pony.orm import select, desc, db_session


@db_session
def by_population(top_count: int):
    return json.dumps([[c.name, c.population] for c in
                       select(c for c in Country).order_by(desc(Country.population)).limit(top_count)[:]])
