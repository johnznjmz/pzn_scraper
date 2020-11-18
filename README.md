# PZN scraper

## Search with PZN and extract the princing details.

## requirements

pandas
beautifulsoup4==4.9.3
mysql-connector-python==8.0.22
requests==2.25.0
urllib3==1.26.2

## For PZN number:
1. PZN
2. Competitor_Name
3. Competitor_price
6. Versandcost
7. Gesamtkosten
8. Created_at

## Usage
### Change/add path to .csv file containing pzn number, (PZN_Ö.csv)

### Run the script pzn_scraper.py

Created basic scraping script for searching with pzn and can view the pricing details of competitor.
currently one can search for pricing details data which belongs to a pzn in apomio.de.
The data is then stored to a db,'pzn_price.db 
