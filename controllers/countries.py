import json

from pony.orm import select, exists, db_session

from data import Country


@db_session
def countries_by_language(language):
    return json.dumps(
        {
            c.name: {
                lc.category: [
                    l.language for l in lc.languages
                ]
                for lc in c.language_categories
            }
            for c in select(c for c in Country
                            if exists(
                                lc for lc in c.language_categories
                                if exists(
                                    l for l in lc.languages if l.language.startswith(language)
                                )
                            )
                            )
        }
    )


@db_session
def countries_by_time_zone(time_zone):
    return json.dumps(
        [
            {c.name: c.time_zone}for c in select(c for c in Country if time_zone in c.time_zone)
        ]
    )


@db_session
def countries_by_government(government):
    return json.dumps(
        [
            {c.name: c.government} for c in select(c for c in Country if government in c.government)
        ]
    )
