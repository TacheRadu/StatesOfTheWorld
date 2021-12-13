import json
from data.country import Country
from pony.orm import select, desc, db_session


@db_session
def by_population(top_count: int):
    return json.dumps(
        {
            c.name: c.population
            for c in select(c for c in Country).order_by(desc(Country.population)).limit(top_count)[:]
         }
    )


@db_session
def by_density(top_count: int):
    return json.dumps(
        {
            c.name: str(c.density) + '/km2'
            for c in select(c for c in Country).order_by(desc(Country.density)).limit(top_count)[:]
        }
    )


@db_session
def by_area(top_count: int):
    return json.dumps(
        {
            c.name: str(c.surface) + ' km2'
            for c in select(c for c in Country).order_by(desc(Country.surface)).limit(top_count)[:]
        }
    )


@db_session
def by_number_of_neighbours(top_count: int):
    return json.dumps(
        {
            c.name: [n.name for n in c.neighbours]
            for c in select(c for c in Country).order_by(lambda c: desc(len(c.neighbours))).limit(top_count)[:]
        }
    )
