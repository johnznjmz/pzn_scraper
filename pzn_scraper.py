import re
import sqlite3
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

date = datetime.now()

conn = sqlite3.connect('pzn_price.db')
c = conn.cursor()

pzns = pd.read_csv("PZN_Ö.csv") #Edit-- copy paste the your file path, file should contain column 'pzn'

#create a list of urls for every pzn and save to the list 'urls'
urls = []

for pzn in pzns['pzn']:
    query_urls = "https://www.apomio.de/suche?query=" + str(pzn)
    mehr_angebote_url = "https://www.apomio.de/preisvergleich-zeige-alle-angebote/" + str(pzn)

    urls.append(query_urls)
    urls.append(mehr_angebote_url)

#parse each url using Beautifulsoup and create a dataframe
def parse(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")

    df = pd.DataFrame(columns=['PZN',
                               'Competitor_name',
                               'Competitor_shop_price',
                               'Versand_cost',
                               'Gesamtkosten',
                               'Last_preis_update',
                               'Created_at'])

    for each in soup.find_all('div', id=re.compile("comparisonRow")):  #Find div with matching id with "comparisonRow"
        try:
            competitor_name = each.find(class_='w-5/6 block text-xs text-black-darker mb-2').text.replace('\n', '')  #find class text, While none append 'None'
        except:
            competitor_name = 'None'
        try:
            competitor_shop_price = each.find(class_="text-red text-xl font-bold no-underline block mb-1").text.replace(
                "'", '')
        except:
            competitor_shop_price = 'None'
        try:
            versand_cost = each.find(class_="block text-xs text-black-darker mb-1").text.replace('\n', '')
        except:
            versand_cost = 'None'
        try:
            last_preis_update = each.find(class_="block text-xxs text-black-darker").text.replace('\n', '')
        except:
            last_preis_update = 'None'
        try:
            gesamtkosten = each.find(class_="block text-xs text-black font-medium").text.replace('\n', '')
        except:
            gesamtkosten = 'None'

        updated_at = date.strftime("%d/%m/%Y %H:%M:%S") #scrape time
        pzn_id = re.sub("[^0-9]", "", url) #pznid from url

        data = df.append({'PZN': pzn_id, 'Competitor_name': competitor_name,   # Create datframe 
                          'Competitor_shop_price': competitor_shop_price,
                          'Versand_cost': versand_cost,
                          'Gesamtkosten': gesamtkosten,
                          'Last_preis_update': last_preis_update,
                          'Updated_at': updated_at},
                         ignore_index=True)
    return data


for url in urls:
    product_price = parse(url)

    c.execute(
        'CREATE TABLE IF NOT EXISTS PRICE (PZN,Competitor_Name,Competitor_price,Versand_cost,Gesamtkosten,Last_preis_update,Created at)') #Creates table
    conn.commit()

    product_price.to_sql('PRICE', conn, if_exists='replace', index=False)
