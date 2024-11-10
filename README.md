# Software Architecture and Design Project - Macedonian Stock Exchange

This is a simple web-scraper written using the pure python libraries "requests" and "BeautifulSoup4", 
where the data is stored in a MongoDB Atlas database, or a local CSV file if the user so chooses.

## Basic database structure

There is a shared "tickers" collection, which contains the information on all listed tickers, as well as the latest 
date for which info is available. Each document in this collection has three fields:
- the _id field, which is mandatory in MongoDB Atlas.
- "ticker" field, which contains the name of the ticker (rather, its Code)
- "latest_available_date", which contains the latest date for which the database holds information.

### Ticker collections

Aside from the shared collection above, each individual ticker has its own collection, where we store the scraped rows
of data. Each ticker's collection is titled by its code. For example, for the ticker ADIN,
the collection will be titled "ADIN"

The documents in these collections share the same format, i.e. they contain the fields specified in the scraped table.
Other than the necessary transformations, the Database also stores each date as a Timestamp field, so that the program
may be able to query the latest available date

## CSV file

For the purposes of the Homework assignment, the program allows the user to write the raw output to a local .csv file.
The information within is unprocessed, but organized alphabetically by ticker code and sorted by date from earliest to latest.


### Team members
- Nikola Janev 221575
- Marko Minovski 221552
- Ermal Baki 221543