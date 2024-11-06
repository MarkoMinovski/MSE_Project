import requests
from bs4 import BeautifulSoup

s = 'mississipi'
old = 'iss'
new = 'XXX'
maxreplace = 1

intermediary = s.rsplit(old, maxreplace)

result = new.join(intermediary)

print(result)
