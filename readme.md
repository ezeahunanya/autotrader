# Autotrader

Autotrader analyses car feature data from thee autotrader website. This project
is split into to three sections:

- Gathering data into a database
- EDA
- Modeling

[Autotrader_scraper](/autotrader_scraper) contains a scrapy project to gather 
car infomation from the autotrader website and store it inside a database.

## Installation

To run this project install [python](https://www.python.org/downloads/). 
Clone the GitHub repository by running the following in the command line:
'''
git clone https://github.com/ezeahunanya/autotrader.git
'''
Create a new environment and pip install the packages in the >>>>requirements.txt file.

To run the scraper, change into the autotrader_scraper directory. Then run the 
following command from the command line:

'''
scrapy crawl autotrader
'''

