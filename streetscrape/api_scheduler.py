from scrapyd_api import ScrapydAPI
from dotenv import dotenv_values, find_dotenv
import time
from streetscrape.headless_browsing_scraper import HeadlessBrowsingScraper

env = dotenv_values(find_dotenv('scrapyd.env'))
print("url: %s" % env['url'])


scrapyd = ScrapydAPI(env['url'],auth=(env['username'],env['password']))

scrapyd.schedule('default','swingtradebot')
scrapyd.schedule('default','thestreet')
scrapyd.schedule('default','zacks')
scrapyd.schedule('default','gurufocus')
scrapyd.schedule('default','stocktwits')

time.sleep(5)
hbs = HeadlessBrowsingScraper('gurufocus')
hbs.start()
