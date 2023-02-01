import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.items import GuruFocusItem
from streetscrape.pipelines import StreetscrapePipeline
import re
from dotenv import find_dotenv, dotenv_values

class GuruFocusSpider(CrawlSpider):
    name = 'gurufocus'
    allowed_domains = ['www.gurufocus.com']
    custom_settings = {}
    if dotenv_values(find_dotenv())['USE_PROXIES'] == '1':
        custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'streetscrape.middlewares.StreetscrapeDownloaderMiddleware': 543,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy_proxies.RandomProxy': 100,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        }
    }



    def __init__(self, *args, **kwargs):
        super(GuruFocusSpider,self).__init__(*args,**kwargs)
        self.unscrapable = []

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
            else:
                self.unscrapable.append(response.request.url)
        except:
            pass





