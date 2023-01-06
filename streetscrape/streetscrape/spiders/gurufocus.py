import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.items import GuruFocusItem
from streetscrape.pipelines import StreetscrapePipeline
import re

class GuruFocusSpider(CrawlSpider):
    name = 'gurufocus'
    allowed_domains = ['www.gurufocus.com']

    def start_requests(self):
        pipeline = StreetscrapePipeline()
        queries = pipeline.get_symbols()
        for query in queries:
            [symbol,name] = query
            url = "https://www.gurufocus.com/stock/%s/summary" % symbol
            yield scrapy.Request(url=url,callback=self.parse, meta={'symbol':symbol})

    def parse(self,response):
        item = GuruFocusItem()
        symbol = response.meta['symbol']
        gf_score = None

        gf_score_data = response.xpath('//script[contains(text(),"gf_score")]/text()').extract_first()
        other_rank_data = response.xpath('//div[contains(@class,"flex-center")]/span/span[1]/text()').extract()
        price_data = response.xpath('//div[@class="m-t-xs"]/span[contains(@class,"t-body-sm")]/text()').extract_first()

        try:
            [balancesheet,growth,momentum,profitability,value] = other_rank_data
            price = re.search("([\d\.]+)",price_data).group(1)
            result = re.search("gf_score\:(\d+)",gf_score_data)
            if result is not None:
                gf_score = result.group(1)
                item['symbol'] = symbol
                item['price_at_rating'] = price
                item['momentum'] = momentum
                item['value'] = value
                item['growth'] = growth
                item['profitability'] = profitability
                item['balancesheet'] = balancesheet
                item['quant'] = gf_score
                yield item
        except:
            pass





