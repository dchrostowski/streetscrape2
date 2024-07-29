import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.items import GuruFocusItem, UnscrapableItem
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
        price_data = response.xpath('//div[@class="m-t-xs"]/span[contains(text(),"$")]/text()').extract_first()

        column_header_map = {
            'growth': 'Growth Rank',
            'momentum': 'Momentum Rank',
            'profitability': 'Profitability Rank',
            'balancesheet': 'Financial Strength',
            'value': 'GF Value Rank',
        }

        for column, header in column_header_map.items():
            xpath1 = "//h2/a[contains(text(),'%s')]/text()" % header
            xpath2 = "//h2[contains(text(),'%s')]/text()" % header
            xpath3 = "//h2/a[contains(text(),'%s')]/parent::h2/parent::div/div/span/span[1]/text()" % header
            try:
                headerValue = response.xpath(xpath1).extract_first()
                if headerValue is not None:
                    item[column] = response.xpath(xpath3).extract_first()
                else:
                    headerValue = response.xpath(xpath2).extract_first()
                    if headerValue is not None:
                        item[column] = 0

            except Exception as e:
                print("exception: %s" % e)
                us_item = UnscrapableItem()
                us_item['url'] = response.request.url
                us_item['symbol'] = symbol
                us_item['site'] = self.name
                print("handing off to headless browser for %s:" % symbol)
                print(us_item)
                yield us_item

        if len(item.keys()) == 5:
            result = re.search("gf_score\:(\d+)",gf_score_data)
            if result is not None:
                gf_score = result.group(1)
                price = re.search("([\d\.]+)",price_data).group(1)
                item['symbol'] = symbol
                item['price_at_rating'] = price
                item['quant'] = gf_score
                print(item)
                yield item
            else:
                us_item = UnscrapableItem()
                us_item['url'] = response.request.url
                us_item['symbol'] = symbol
                us_item['site'] = self.name
                print("handing off to headless browser for %s:" % symbol)
                print(us_item)
                yield us_item
        else:
            print("no data for %s" % symbol)
            us_item = UnscrapableItem()
            us_item['url'] = response.request.url
            us_item['symbol'] = symbol
            us_item['site'] = self.name
            print("handing off to headless browser for %s:" % symbol)
            print(us_item)
            yield us_item