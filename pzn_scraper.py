import time
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#web driver options
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

# webdriver path
driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\chromedriver.exe')
driver.get('https://www.apomio.de/')
driver.maximize_window()
time.sleep(5)

# urls = []
competitor_name_list = []
competitor_shop_price_list = []
competitor_Versand_frei_ab_list = []
competitor_Grundpreis_list = []
competitor_Versand_cost_list = []
competitor_Gesamtkosten_list = []

# Load csv file
pzn_data = pd.read_csv("PZN_Ö.csv")

for pzn in pzn_data['pzn']:

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "apomio-search")))
    search = driver.find_element(By.ID, "apomio-search")
    search.send_keys(pzn)
    search.send_keys(Keys.ENTER)
    time.sleep(5)
    #elem = driver.find_element_by_partial_link_text("alle-angebote")
    #elem.click()
    #time.sleep(10)

    # mehr ="https://www.apomio.de/preisvergleich-zeige-alle-angebote/"+str(pzn)
    # html = "https://www.apomio.de/suche?query="+str(pzn)
    # urls.append(html)
    # urls.append(mehr)

    # for url in urls:
    url = driver.current_url
    soup = BeautifulSoup(url)
    # page = requests.get(url)
    # time.sleep(5)
    # soup = BeautifulSoup(page.text, 'html.parser')

    price_tag = soup.find_all("div", class_="w-1/2 pr-3 xl:pr-0 text-right")
    name_tag = soup.find_all("span", class_="w-5/6 block text-xs text-black-darker mb-2")
    price_tag_cheapest = soup.find_all("div", class_="w-1/2 pr-3 xl:pr-0 text-right c-best-price")

    for i in name_tag:
        competitor_name = i.get_text("\n", strip=True)
        competitor_name_list.append(competitor_name)

    for j in price_tag_cheapest:
        competitor_shop_price_cheapest = j.find("a", attrs={
            'class': 'text-red text-xl font-bold no-underline block mb-1'}).get_text("'", strip=True)
        Versand_frei_ab = j.find('span', attrs={'class': 'hidden md:block text-xs text-black-darker mb-1'}).get_text(
            strip=True)
        Grundpreis = j.find('span', attrs={'class': 'hidden md:block text-xs text-black-darker mb-1'}).find_next(
            "span").get_text(strip=True)
        Versand_cost = j.find('span', attrs={'class': 'block text-xs text-black-darker mb-1'}).get_text(strip=True)
        Gesamtkosten = j.find('span', attrs={'class': 'block text-xs text-black font-medium'}).get_text("\n",
                                                                                                        strip=True)
        competitor_shop_price_list.append(competitor_shop_price_cheapest)
        Versand_frei_ab = Versand_frei_ab.strip('Versand frei ab ')
        competitor_Versand_frei_ab_list.append(Versand_frei_ab)
        Grundpreis = Grundpreis.strip('Grundpreis: je 100 Stück').strip('Grundpreis: je 100 g').strip(
            'Grundpreis: je 100 ml')
        competitor_Grundpreis_list.append(Grundpreis)
        Versand_cost = Versand_cost.strip('Versand')
        competitor_Versand_cost_list.append(Versand_cost)
        Gesamtkosten = Gesamtkosten.strip('Gesamtkosten')
        competitor_Gesamtkosten_list.append(Gesamtkosten)

    for k in price_tag:
        competitor_shop_price = k.find("a",
                                       attrs={'class': 'text-red text-xl font-bold no-underline block mb-1'}).get_text(
            "'", strip=True)
        Versand_frei_ab = k.find('span', attrs={'class': 'hidden md:block text-xs text-black-darker mb-1'}).get_text(
            strip=True)
        Grundpreis = k.find('span', attrs={'class': 'hidden md:block text-xs text-black-darker mb-1'}).find_next(
            "span").get_text(strip=True)
        Versand_cost = k.find('span', attrs={'class': 'block text-xs text-black-darker mb-1'}).get_text(strip=True)
        Gesamtkosten = k.find('span', attrs={'class': 'block text-xs text-black font-medium'}).get_text("\n",
                                                                                                        strip=True)
        competitor_shop_price_list.append(competitor_shop_price)
        Versand_frei_ab = Versand_frei_ab.strip('Versand frei ab ')
        competitor_Versand_frei_ab_list.append(Versand_frei_ab)
        Grundpreis = Grundpreis.strip('Grundpreis: je 100 Stück').strip('Grundpreis: je 100 g').strip(
            'Grundpreis: je 100 ml')
        competitor_Grundpreis_list.append(Grundpreis)
        Versand_cost = Versand_cost.strip('Versand')
        competitor_Versand_cost_list.append(Versand_cost)
        Gesamtkosten = Gesamtkosten.strip('Gesamtkosten')
        competitor_Gesamtkosten_list.append(Gesamtkosten)

now = datetime.now()
date = now.strftime("%d/%m/%Y %H:%M:%S")

# create dataframe
data = pd.DataFrame(
    {'PZN': pzn,
     'competitor_name': competitor_name_list,
     'competitor_shop_price': competitor_shop_price_list,
     'Versand_frei_ab': competitor_Versand_frei_ab_list,
     'Grundpreis': competitor_Grundpreis_list,
     'Versand_cost': competitor_Versand_cost_list,
     'Gesamtkosten': competitor_Gesamtkosten_list,
     'Created_at': date,
     })

# Save dataframe to db
conn = sqlite3.connect('pzn_price.db')
c = conn.cursor()

c.execute(
    'CREATE TABLE IF NOT EXISTS PRICE (PZN,Competitor_Name,Competitor_price,Versand frei ab,Grundpreis,Versandcost,Gesamtkosten,Created at)')
conn.commit()

data.to_sql('PRICE', conn, if_exists='replace', index=False)
