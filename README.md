# States of the World

The purpose of this project is to scrape wikipedia for collecting data on all the countries, saving them in a database, and then exposing an api for showing country data.

You can run the scrapper from [scrapper.py](https://github.com/TacheRadu/StatesOfTheWorld/blob/main/scrapper.py).
The database configuration could be changed from the [init file](https://github.com/TacheRadu/StatesOfTheWorld/blob/main/data/__init__.py)

The server can be run from [server.py](https://github.com/TacheRadu/StatesOfTheWorld/blob/main/server.py), and it's using Flask.

The api has the following routes:

`/top/<top_count>/<criteria>`: Shows the first `<top_count>` countries following criteria. The criteria can be: `population`, `density`, `surface`, `number-of-neighbours`.

`/countries/<criteria>/<value>`: Shows the countries having `<criteria>` equal to `<value>`. The criteria can be: `language`, `time-zone`, `government`, `driving-side`.

`/country/<country_name>`: Shows information about a specific country.
