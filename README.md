#PZN scraper

Search with PZN and extract the princing details.

##requirements

beautifulsoup==4 4.9.3 selenium==3.141.0 .0 db-sqlite==3 0.0.1

##For PZN number:
1.PZN
2.Competitor_Name
3.Competitor_price
4.Versand_frei_ab
5.Grundpreis
6.Versandcost
7.Gesamtkosten
8.Created_at



#Change path to webserver and .csv file contaaining pzn number 

#Run the script pzn_scraper.py

Created basic scraping script for searching with pzn and can view the pricing details of competitor.
currently one can search for pricing details data which belongs to a pzn in apomio.de.
The data is then stored to a db,'pzn_price.db'

Use selenium for scraping page, running time is more.

potential improvemnets: use Requests to loop throug list of urls 
