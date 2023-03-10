import scrapy
from scrapy.spiders import CrawlSpider
from streetscrape.items import SecurityItem

class SwingtradebotSpider(CrawlSpider):
    name = 'swingtradebot'
    allowed_domains = ['swingtradebot.com']


    def start_requests(self):
        url = 'https://swingtradebot.com/equities?min_vol=250000&min_price=10.0&max_price=999999.0&adx_trend=&grade=&rsi_comparator=&rsi_value1=&include_etfs=2&html_button=as_html'
        request = scrapy.Request(url=url, callback=self.parse)
        yield request

    def parse(self, response):
        table_rows = response.xpath('//table/tbody/tr')

        for row in table_rows:
            item = SecurityItem()
            symbol = row.xpath('td[2]/a/text()').extract_first()
            company_name = row.xpath('td[4]/a/text()').extract_first().replace(',','')
            closing_price = row.xpath('td[5]/text()').extract_first()
            item['symbol'] = symbol
            item['name'] = company_name
            print("%s %s %s" % (symbol,company_name, closing_price) )
            yield item

        next = response.xpath('//div[@class="btn-group"]/a[contains(@class,"next")]/@href').extract_first()
        if next:
            next = 'https://swingtradebot.com/' + next
            yield scrapy.Request(url=next, callback=self.parse)


