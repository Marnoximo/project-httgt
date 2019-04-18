# Scrape the data of game ranking of the last 3 months on metacritic website
import bs4
import urllib
import requests
import csv
import numpy as np

# Metacritic URL
url = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?sort=desc&page='
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
# Page number
num_page = 0
# Data array
data = []
data.append(['title','platform','metascore','userscore','release_date'])

# Scraping loops
while True:
    print('Read page: ', num_page)
    urlfull = url+str(num_page)
    request = urllib.request.Request(urlfull, None, headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    
    table = soup.find('ol', class_='list_products list_product_condensed')
    if table is None:
        break
    for r in table.find_all('div', class_='product_wrap'):
        line = []
        title_platform = r.find('a').getText().strip('\n').strip().replace('  ','').replace(';',':').split('\n')
        line.append(title_platform[0])
        line.append(title_platform[1].strip(')').strip('()'))
        line.append(r.find('div', class_='metascore_w').getText())
        span = r.find_all('span')
        line.append(span[1].getText())
        line.append(span[3].getText())
        data.append(line)
    num_page = num_page + 1
print('finish surf through all pages')

# Save in csv file
with open('./data/metacritic.csv', 'w') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(data)

