PZN scraper

Search with PZN and extract the princing details.

requirements

BeautifulSoup==1.12.0 selenium==1.1.2 BeautifulSoup==2.1.0 sqlite3==1.3.17 

For PZN number:
PZN
Competitor_Name
Competitor_price
Versand_frei_ab
Grundpreis
Versandcost
Gesamtkosten
Created_at

run the script pzn_scraper.py

change path to webserver and .csv file contaaining pzn number 

Created basic scraping script for searching with pzn and can view the pricing details of competitor.

Currently one can search for pricing details data which belongs to a pzn in apomio.de.

The data is then stored to a db,'pzn_price.db'

Used selenium for scraping page, running time is more.

potential improvemnets: use url requests to loop throug list of urls 
