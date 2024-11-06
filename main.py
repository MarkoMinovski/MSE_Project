import sys

from datetime import datetime, timedelta
from TickerScraper import TickerScraper
from DBClient import database as db

TEN_YEARS_PRIOR = datetime.today() - timedelta(days=(365 * 10) - 1)

if __name__ == '__main__':
    initial_url = "https://www.mse.mk/mk/stats/symbolhistory/MPT"

    raw_tickers_scraper = TickerScraper(initial_url)

    # First part of the pipeline
    tickers_filtered = raw_tickers_scraper.initial_scrape()

    if tickers_filtered is None:
        print("Error in the first part of the pipeline")
        sys.exit(1)

    # Our MongoDB database is literally called database

    existing_tickers = db.list_collection_names()
    ticker_name_last_date_pairs = []
    # list of tuples, with ticker name and last available date as the two elements

    # Second part of the pipeline
    for ticker in tickers_filtered:
        # We have a collection in our database that holds information about each ticker and the latest date for
        # which we have scraped data
        ticker_info_collection = db["tickers"]

        if ticker not in existing_tickers:

            new_doc = {
                "ticker": ticker,
                "last_date_info": TEN_YEARS_PRIOR
            }

            ticker_info_collection.insert_one(new_doc)
            ticker_name_last_date_pairs.append((ticker, TEN_YEARS_PRIOR))

        elif ticker in existing_tickers:

            name_last_date_pair = ticker_info_collection.find_one({"ticker": ticker})

            tmp_tuple = (name_last_date_pair["ticker"], name_last_date_pair["last_date_info"])

            ticker_name_last_date_pairs.append(tmp_tuple)

    # TODO: TRANSFORM ABOVE CODE TO BE MORE MODULAR, AND EXPAND IT
