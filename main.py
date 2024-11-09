import sys

from datetime import datetime, timedelta, date
from TickerScraper import TickerScraper
from DBClient import database as db
from Tablescraper import Tablescraper

TEN_YEARS_PRIOR = datetime.today() - timedelta(days=(365 * 10) - 1)
TODAY = date.today()

if __name__ == '__main__':
    initial_url = "https://www.mse.mk/mk/stats/symbolhistory/MPT"

    raw_tickers_scraper = TickerScraper(initial_url)

    # First part of the pipeline
    tickers_filtered = raw_tickers_scraper.initial_scrape()

    if tickers_filtered is None:
        print("Error in the first part of the pipeline")
        sys.exit(1)

    # existing_tickers = db.list_collection_names()
    ticker_name_last_date_pairs = []
    # list of tuples, with ticker name and last available date as the two elements

    # We have a collection in our database that holds information about each ticker and the latest date for
    # which we have scraped data
    ticker_info_collection = db["tickers"]

    # Second part of the pipeline
    for ticker in tickers_filtered:
        query_result = ticker_info_collection.find_one({"ticker": ticker})

        if query_result is None:

            new_doc = {
                "ticker": ticker,
                "last_date_info": TEN_YEARS_PRIOR
            }

            ticker_info_collection.insert_one(new_doc)
            ticker_name_last_date_pairs.append((ticker, TEN_YEARS_PRIOR))

        else:
            tmp_tuple = (query_result["ticker"], query_result["last_date_info"])
            ticker_name_last_date_pairs.append(tmp_tuple)

    # TODO: TRANSFORM ABOVE CODE TO BE MORE MODULAR, AND EXPAND IT

    # third part of the pipeline

    # this list will be a list of additional boolean values for each index of the tuples list above. example:
    # is_up_to_date[0] = True
    # means the ticker_last_date pair is up-to-date, and we don't need to scrape for them

    is_up_to_date = []

    # first we need to build this list
    for ticker_name_last_date_pair in ticker_name_last_date_pairs:
        is_up_to_date.append(False)

    # PyCharm says to simplify this expression, but this reads more clearly

    # Basically continuously call the Tablescraper module while any remaining ticker value is NOT up-to-date

    # For now though, let's just test the module first

    Tablescraper.scrape_table(ticker_name_last_date_pairs[0][0], ticker_name_last_date_pairs[0][1])
