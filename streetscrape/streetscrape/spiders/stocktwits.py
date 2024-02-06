import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.pipelines import StreetscrapePipeline
from streetscrape.items import StocktwitsItem

import json

class StockTwitsSpider(CrawlSpider):
    name = 'stocktwits'
    allowed_domains = ['stocktwits.com']

    def start_requests(self):
        pipeline = StreetscrapePipeline()
        queries = pipeline.get_symbols()
        for query in queries:
            (symbol,name) = query
            url = "https://api-gw-prd.stocktwits.com/sentiment-api/%s/details" % symbol
            # https://ql.stocktwits.com/intraday?symbol=PHM
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        try:
            data = json.loads(response.text)['data']['sentiment']['now']
            print(data['valueNormalized'])

            
            yield data
        except Exception as e:
            print(e)


