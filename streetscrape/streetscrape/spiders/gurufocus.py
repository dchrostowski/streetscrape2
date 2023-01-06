import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from streetscrape.items import ZacksItem
from streetscrape.pipelines import StreetscrapePipeline
import re

from IPython import embed

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
        item = {}
        symbol = response.meta['symbol']
        gf_score = None

        gf_score_data = response.xpath('//script[contains(text(),"gf_score")]/text()').extract_first()
        other_rank_data = response.xpath('//div[contains(@class,"flex-center")]/span/span[1]/text()').extract()

        try:
            [balancesheet,growth,momentum,profitability,value] = other_rank_data

            result = re.search("gf_score\:(\d+)",gf_score_data)
            if result is not None:
                gf_score = result.group(1)
                item['symbol'] = symbol
                item['momentum'] = momentum
                item['value'] = value
                item['growth'] = growth
                item['profitability'] = profitability
                item['balancesheet'] = balancesheet
                item['quant'] = gf_score

                print(item)
        except:
            pass





