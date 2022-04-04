from re import S
from bs4 import BeautifulSoup
import requests
import json

def get_row_data(row_data):
    if row_data.find('li'):
        return [li.get_text(" ", strip=True).replace("\xa0"," ") for li in row_data.find_all('li')]  
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0"," ")



def get_info_box(url):

    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.content, 'lxml')
    infobox = soup.find('table',class_='infobox vevent')
    allRows = infobox.find_all('tr')
    
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


    return movie_info




moviePageLink = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'

html_text = requests.get(moviePageLink)
soup = BeautifulSoup(html_text.content, 'lxml')
movieYears = soup.find_all('span',class_='mw-headline')
allMovies = soup.select(".wikitable.sortable i a")
print(f"Total movies: {len(allMovies)}")
baseUrl = 'https://en.wikipedia.org/' 
movie_info_list = []

for index, movie in enumerate(allMovies):
    try:
        relative_path = movie['href']
        fullPath = baseUrl + relative_path
        title = movie['title']
        movie_info_list.append(get_info_box(fullPath))
    except Exception as e:
        print(movie.get_text())
        print(e)

print(f"Total movies in file: {len(movie_info_list)}")


def save_data(title,data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)


def load_data(title):
    with open(title,encoding="utf-8") as f:
        return json.load(f)


save_data('disney_data.json',movie_info_list)

# for table in allTables:
#     tableBody = table.find('tbody')
#     allRows = tableBody.find_all('tr')
#     for rows in allRows:
#         tableData = rows.find_all('td')
#         for index, data in enumerate(tableData):
#             if index == 1:
#                 print(data)
