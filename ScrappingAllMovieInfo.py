from re import S
from bs4 import BeautifulSoup
import requests


moviePageLink = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'

html_text = requests.get(moviePageLink)
soup = BeautifulSoup(html_text.content, 'lxml')
movieYears = soup.find_all('span',class_='mw-headline')
allTables = soup.find_all('table', class_='wikitable sortable jquery-tablesorter')
all_movie_info = {}
header = soup.find('th',class_='headerSort')

allTableRows = allTables.find_all('tr')

for tableRow in allTableRows:
    tablehead = tableRow.find_all('td')