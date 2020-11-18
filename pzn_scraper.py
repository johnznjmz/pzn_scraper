import re
import sqlite3
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

date = datetime.now()
conn = sqlite3.connect('pzn_price.db')  # Db name
c = conn.cursor()

pzns = pd.read_csv("PZN_Ö.csv")  # Edit-- copy paste the your file path, file should contain column 'pzn'
urls = []  # create a list of urls for every pzn and save to the list 'urls'

for pzn in pzns['pzn']:
    query_urls = "https://www.apomio.de/suche?query=" + str(pzn)
    mehr_angebote_url = "https://www.apomio.de/preisvergleich-zeige-alle-angebote/" + str(pzn)

    urls.append(query_urls)
    urls.append(mehr_angebote_url)


# parse each url using BeautifulSoup
def parse(url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        'referer': 'https://www.google.com/'}
    html = requests.get(url, headers=header)
    parse_text = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    return parse_text


# Create a data frame from parse text
def create_table():
    soup = parse(url)

    data = pd.DataFrame(columns=['PZN',
                                 'Competitor_name',
                                 'Competitor_shop_price',
                                 'Versand_cost',
                                 'Gesamtkosten',
                                 'Last_preis_update',
                                 'Created_at'])

    for each in soup.find_all('div', id=re.compile("comparisonRow")):  # Find div with matching id "comparisonRow"
        try:
            competitor_name = each.find(class_='w-5/6 block text-xs text-black-darker mb-2').text.replace('\n',
                                                                                                          '')  # Find class text, While none append 'None'
        except:
            competitor_name = 'None'
        try:
            competitor_shop_price = each.find(class_="text-red text-xl font-bold no-underline block mb-1").text.replace(
                "\n", '').replace(" ", "")
        except:
            competitor_shop_price = 'None'
        try:
            versand_cost = each.find(class_="block text-xs text-black-darker mb-1").text.replace(
                "Versand", "").replace("'", "")
        except:
            versand_cost = 'None'
        try:
            last_preis_update = each.find(class_="block text-xxs text-black-darker").text.replace(
                "Preis vom", "").replace("Preis kann jetzt höher sein.**", "")
        except:
            last_preis_update = 'None'
        try:
            gesamtkosten = each.find(class_="block text-xs text-black font-medium").text.replace(
                "\n", '').replace("Gesamtkosten", "").replace(" ", "")
        except:
            gesamtkosten = 'None'

        created_at = date.strftime("%d/%m/%Y %H:%M:%S")  # scrape time
        pzn_id = re.sub("[^0-9]", "", url)  # pzn_id from url

        data = data.append({'PZN': pzn_id, 'Competitor_name': competitor_name,
                            'Competitor_shop_price': competitor_shop_price,
                            'Versand_cost': versand_cost,
                            'Gesamtkosten': gesamtkosten,
                            'Last_preis_update': last_preis_update,
                            'Created_at': created_at},
                           ignore_index=True)
    return data


# Create table
for url in urls:
    product_price = create_table()

    c.execute(
        'CREATE TABLE IF NOT EXISTS PRICE ("PZN" varchar NOT NULL,"Competitor_Name" varchar NOT NULL,"Competitor_shop_price" varchar NOT NULL,"Versand_cost" varchar NOT NULL,"Gesamtkosten" varchar NOT NULL,"Last_preis_update" varchar NOT NULL,"Created_at" varchar NOT NULL)')
    conn.commit()

    product_price.to_sql('PRICE', conn, if_exists='append', index=False)