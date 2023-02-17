from scrapyd_api import ScrapydAPI
from dotenv import dotenv_values, find_dotenv
import time

creds = dotenv_values(find_dotenv('scrapyd.env'))


scrapyd = ScrapydAPI('http://localhost:6800',auth=(creds['username'],creds['password']))

scrapyd.schedule('default','swingtradebot')
scrapyd.schedule('default','thestreet')
scrapyd.schedule('default','zacks')
scrapyd.schedule('default','gurufocus')


#ingest_gurufocus()