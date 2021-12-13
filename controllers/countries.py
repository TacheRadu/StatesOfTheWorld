import json

from pony.orm import select, exists, db_session, set_sql_debug

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
