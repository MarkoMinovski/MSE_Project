import sys

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta
from scraper import TickerScraper

TEN_YEARS_PRIOR = datetime(2024, 11, 2) - timedelta(days=365 * 10)

uri = "mongodb+srv://marko_m:HhfpCcGObwf7Huxn@maincluster.zwq2b.mongodb.net/?retryWrites=true&w=majority&appName=MainCluster"

client = MongoClient(uri, server_api=ServerApi('1'))

if __name__ == '__main__':
    initial_url = "https://www.mse.mk/mk/stats/symbolhistory/MPT"

    raw_tickers_scraper = TickerScraper(initial_url)

    # First part of the pipeline
    tickers_filtered = raw_tickers_scraper.initial_scrape()

    if tickers_filtered is None:
        print("Error in the first part of the pipeline")
        sys.exit(1)

    # Our MongoDB database is literally called database
    database = client["database"]

    existing_tickers = database.list_collection_names()
    ticker_name_last_date_pairs = []
    # list of tuples, with ticker name and last available date as the two elements

    # Second part of the pipeline
    for ticker in tickers_filtered:
        # We have a collection in our database that holds information about each ticker and the latest date for
        # which we have scraped data
        ticker_info_collection = database["tickers"]

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