from bs4 import BeautifulSoup
import requests

moviePageLink = 'https://en.wikipedia.org/wiki/Toy_Story_3'

html_text = requests.get(moviePageLink)
soup = BeautifulSoup(html_text.content, 'lxml')
infobox = soup.find('table',class_='infobox vevent')
allRows = infobox.find_all('tr')
# for row in allRows:
#     print(row.prettify())

def get_row_data(row_data):
    if row_data.find('li'):
        return [li.get_text(" ", strip=True).replace("\xa0"," ") for li in row_data.find_all('li')]  
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0"," ")

movie_info = {}
for index,row in enumerate(allRows):
    if index == 0:
        movie_info['title'] = row.find("th").get_text(" ", strip=True)
    elif index == 1:
        continue
    else:
        content_key = row.find('th').get_text(" ", strip=True)
        content_value = get_row_data(row.find("td"))
        movie_info[content_key] = content_value

print(movie_info)
