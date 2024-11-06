from DBClient import database as db
import requests
from bs4 import BeautifulSoup
from tablerow import TableRow
from datetime import datetime, timedelta

DEFAULT_URL = "https://www.mse.mk/mk/stats/symbolhistory/MPT"
TODAY = datetime.today()


def is_less_than_year_ago(date):
    one_year_ago = TODAY - timedelta(days=364)
    if date < one_year_ago:
        return True
    else:
        return False


def reformat_delimiters(table_row_object):
    pass


# Abstract class. Methods only, no fields needed
class TableScraper:
    @staticmethod
    def ScrapeTable(ticker_code, latest_date):
        response = TableScraper.send_post_request(ticker_code, latest_date)
        soup = BeautifulSoup(response.content, "html.parser")

        table_rows = soup.find_all('tr')

        # HTML structure of stock exchange page:
        # each <tr> has exactly 9 child <td> tags
        for row in table_rows:
            children = row.find_all('td')

            table_row_obj = TableRow()

            table_row_obj.date = children[0].text
            table_row_obj.last_trade_price = children[1].text
            table_row_obj.max = children[2].text
            table_row_obj.min = children[3].text
            table_row_obj.avg = children[4].text
            table_row_obj.percentage_change_as_decimal = children[5].text
            table_row_obj.volume = children[6].text
            table_row_obj.BEST_turnover_in_denars = children[7].text
            table_row_obj.total_turnover_in_denars = children[8].text

    @staticmethod
    def send_post_request(ticker_code, latest_date):
        from_date = latest_date
        if is_less_than_year_ago(from_date):
            days_between = abs(TODAY - from_date)
            to_date = from_date + timedelta(days=days_between.days)
        else:
            to_date = from_date + timedelta(days=364)

        header = {
            "content_type": "application/x-www-form-urlencoded"
        }

        from_date_string = str(from_date.day) + "." + str(from_date.month) + "." + str(from_date.year)
        to_date_string = str(to_date.month) + "." + str(to_date.day) + "." + str(to_date.year)

        payload = {
            "FromDate": from_date_string,
            "ToDate": to_date_string,
            "Code": ticker_code
        }
        server_resp = requests.post(DEFAULT_URL, headers=header, data=payload)

        if server_resp.status_code == 200:
            return server_resp
        else:
            return None
