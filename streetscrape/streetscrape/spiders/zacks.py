import scrapy
from scrapy.spiders import CrawlSpider, Rule
import json
from streetscrape.items import ZacksItem
from streetscrape.pipelines import StreetscrapePipeline

class ZacksSpider(CrawlSpider):
    name = 'zacks'
    allowed_domains = ['www.zacks.com','quote-feed.zacks.com']

    def start_requests(self):
        pipeline = StreetscrapePipeline()
        queries = pipeline.get_symbols()
        for query in queries:
            (symbol,name) = query
            url = "https://www.zacks.com/defer/premium_research_v2.php?premium_string=0&ticker_string=%s&logged_string=0" % symbol
            yield scrapy.Request(url=url,callback=self.parse_vgm, meta={'symbol':symbol})

    def calculate_quant_rating(self,grade,vgm):
        if grade is None:
            return 0
        grade_map = {
            'Strong Buy': 4,
            'Buy': 3,
            'Hold': 2,
            'Sell': 1,
            'Strong Sell': 0,
        }

        vgm_map = {
            'A': 4,
            'B': 3,
            'C': 2,
            'D': 1,
            'F': 0
        }
        rank_num = grade_map[grade]
        vgm_num = vgm_map[vgm]
        final_score = (vgm_num + rank_num)/8 * 100
        return str(round(final_score,2))

    def parse_vgm(self,response):
        vgm = response.xpath('//p[@class="float_right"]/span[contains(@class,"composite_val")]/text()').extract()
        symbol = response.meta['symbol']
        if len(vgm) == 4:
            url = 'https://quote-feed.zacks.com/index.php?t=%s' % symbol
            yield scrapy.Request(url=url,callback=self.parse, meta={'symbol':symbol, 'vgm': vgm})


    def parse(self, response):
        data = json.loads(response.text)
        item = ZacksItem()
        try:
            data = json.loads(response.text)[response.request.meta['symbol']]
            grade = "%s-%s" % (data['zacks_rank'], data['zacks_rank_text'])
            price = data['last']
            (value,growth,momentum,vgm) = response.meta['vgm']
            quant = self.calculate_quant_rating(data['zacks_rank_text'],vgm)

            item['symbol'] = response.request.meta['symbol']
            item['grade'] = grade
            item['price_at_rating'] = price
            item['value'] = value
            item['growth'] = growth
            item['momentum'] = momentum
            item['vgm'] = vgm
            item['quant'] = quant

            yield item
        except Exception as e:
            print(e)

