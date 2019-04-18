# Scrape the data of game ranking of the last 3 months on Game Ranking website

import numpy as np
import urllib
import bs4
import csv
import requests

# Gameranking URL
urlhead = 'https://www.gamerankings.com/browse.html?page='
urltail = '&year=3&numrev=4'

# Data array
data = []
data.append(['platform','title','developer','score','num_of_reviews'])

# Scraping loops
i = 0
while True:
	print('Scrape data from page: ', i)
    source = urllib.request.urlopen(urlhead+str(i)+urltail)
    soup = bs4.BeautifulSoup(source, 'html.parser')
    table = soup.find('table')
    if table is None:
        break
    row = table.find_all('tr')
    for r in row:
        line = []
        l = r.getText().strip('\n').strip().replace('\t','').replace('\r','').replace(';',':').split('\n')
        line.append(l[0])
        line.append(l[1])
        line.append(l[2].split(',')[0])
        temp = l[3].split('%')
        line.append(temp[0])
        line.append(temp[1].replace(' Reviews',''))
        data.append(line)
    i += 1

#Save data as a csv file in data folder
with open('./data/gameranking.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(data)
