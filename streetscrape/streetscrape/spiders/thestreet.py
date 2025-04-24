import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.pipelines import StreetscrapePipeline
from streetscrape.items import TheStreetItem

import json

class ThestreetSpider(CrawlSpider):
    name = 'thestreet'
    allowed_domains = ['www.thestreet.com', 'widgets.tipranks.com']

    def start_requests(self):
        pipeline = StreetscrapePipeline()
        queries = pipeline.get_symbols()
        
        for query in queries:
            (symbol,name) = query
            url = "https://widgets.tipranks.com/api/etoro/dataForTicker?ticker=%s" % symbol
            print("getting %s" % url)
            yield scrapy.Request(url=url,callback=self.parse)


    def calculate_quant_rating(self,grade):
        return int(grade) * 10
    
    def parse(self, response):
        try:
            data = json.loads(response.text)['overview']
            grade = "%s" % data['tipranksStockScore']['score']
            price_at_rating = data['prices'][-1]['p']
            symbol = data['ticker']
            quant = self.calculate_quant_rating(grade)
            item = TheStreetItem()
            item['symbol'] = symbol
            item['grade'] = grade
            item['price_at_rating'] = price_at_rating
            item['quant'] = quant
            print(item)
            yield item
        except Exception as e:
            print(e)
