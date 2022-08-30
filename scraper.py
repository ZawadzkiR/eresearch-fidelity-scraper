import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pickle
import random


symbol = 'AMC'


page_new ='https://eresearch.fidelity.com/eresearch/evaluate/news/basicNews.jhtml?symbols={}&anchor=2_202104171957RTRSNEWSCOMBINED_KBN2C40L7-OUSBS_1'.format(symbol)

list_ = []
page_new = '/eresearch/evaluate/news/basicNews.jhtml?symbols={}'.format(symbol)

for loop in range(500):

#site scrap  
  url ='https://eresearch.fidelity.com'+page_new
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  td= soup.find_all('td', {'valign': 'top'})

  for tds in td:
    try:
      title = tds.find('a').text.replace('\n', '').replace('  ', '')
      date = tds.find('div', {'class': 'source'}).text.replace('\n', '').replace('  ', '').replace('\t', '').replace('  ', '')
      description = tds.find('p').text.replace('\n', '').replace('  ', '')
      list_.append([title, date, description])
    except:
      pass


#find new page
  try:
    page_new= soup.find('span', {'id': 'next-pg', 'title': 'Next Page'}).find('a')['href']
    time.sleep(random.randint(2,6))
  except:
    break

df = pd.DataFrame(list_, columns=['Title', 'Date', 'Description'])
df = df.loc[~df['Title'].isin(['Print', 'Log in for more news'])]
df.to_csv('headers.csv')
