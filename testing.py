from Tablescraper import is_less_than_year_ago
from datetime import datetime, timedelta, time

date = datetime(2024, 7, 12)

if is_less_than_year_ago(date) is True:
    print("Date is less than a year ago")
else:
    print("Error in func")
