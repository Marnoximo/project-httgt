import numpy as np
import urllib
import bs4
import csv
import requests

urlhead = 'https://www.gamerankings.com/browse.html?page='
urltail = '&year=3&numrev=4'

data = []
data.append(['platform','title','developer','score','num_of_reviews'])

i = 0
while True:
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
    
with open('./data/gameranking.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(data)
