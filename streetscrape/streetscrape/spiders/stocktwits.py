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
            url = "https://api-gw-prd.stocktwits.com/sentiment-api/%s/detail" % symbol
            
            yield scrapy.Request(url=url,callback=self.parse_sentiment, meta={'symbol':symbol})

    def parse_price(self, response):
        json_data = json.loads(response.body.decode('utf-8'))
        latest_price_idx = 0

        for price_data in json_data:
            if price_data['StartDate'] is None:
                break
            latest_price_idx +=1

        
        latest_price_data = json_data[latest_price_idx-1]

        price_at_rating = latest_price_data['Open']

        all_data = response.meta['sentiment']
        all_data['price_at_rating'] = price_at_rating
        all_data['symbol'] = response.meta['symbol']

        item = StocktwitsItem()

        item['symbol'] = response.meta['symbol']
        item['price_at_rating'] = price_at_rating
        item['label'] = all_data['label']
        item['label_normalized'] = all_data['labelNormalized']
        item['grade'] = all_data['value']
        item['quant'] = all_data['valueNormalized']

        print(json.dumps(all_data))

        yield item


    def parse_sentiment(self, response):

        json_data = json.loads(response.body.decode('utf-8'))
        sentiment_data = json_data['data']['sentiment']['now']

        if sentiment_data['loaded']:
            price_url = "https://ql.stocktwits.com/intraday?symbol=%s" % response.meta['symbol']
            symbol = response.meta['symbol']
            yield scrapy.Request(url=price_url, callback=self.parse_price, meta={'sentiment': sentiment_data, 'symbol':symbol})

        

        
       


