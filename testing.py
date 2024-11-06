import requests
from bs4 import BeautifulSoup

resp = requests.get("https://www.example.com/")

soup = BeautifulSoup(resp.content, 'html.parser')

div = soup.find_all('div')[0]

second_p = div.find_all('p')[1]

print(second_p)
