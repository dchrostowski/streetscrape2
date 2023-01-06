import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from streetscrape.pipelines import StreetscrapePipeline
from streetscrape.items import TheStreetItem

import json

class ThestreetSpider(CrawlSpider):
    name = 'thestreet'
    allowed_domains = ['www.thestreet.com']

    def start_requests(self):
        pipeline = StreetscrapePipeline()
        queries = pipeline.get_symbols()
        for query in queries:
            (symbol,name) = query
            url = 'https://api.thestreet.com/marketdata/2/1?includePartnerContent=true&includeLatestNews=false&start=0&rt=true&max=10&filterContent=false&format=json&s=%s&includePartnerNews=false' % symbol
            yield scrapy.Request(url=url,callback=self.parse)


    def calculate_quant_rating(self,grade):
        if grade is None:
            return 0
        rating_map = {
            'E+': 0,
            'D-': 1,
            'D': 2,
            'D+': 3,
            'C-': 4,
            'C': 5,
            'C+': 6,
            'B-': 7,
            'B': 8,
            'B+': 9,
            'A-': 10,
            'A': 11,
            'A+': 12
        }
        number_grade = rating_map[grade]
        return str(round(number_grade/12 * 100,2))

    def parse(self, response):
        data = json.loads(response.text)
        try:
            quotes = json.loads(response.text)['response']['quotes']
            for quote in quotes:
                item = TheStreetItem()
                company_name = quote['companyName'].replace(',','')
                symbol = quote['symbol']
                grade = quote['letterGradeRating']
                price = quote['currentPrice']
                quant_rating = self.calculate_quant_rating(grade)

                item['symbol'] = symbol
                item['grade'] = grade
                item['price_at_rating'] = price
                item['quant'] = quant_rating

                yield item

                with open('./csv/thestreet_grades.csv','a') as ofh:
                    ofh.write("%s,%s,%s,%s,%s\n" % (symbol,company_name,grade,price,quant_rating))
        except Exception as e:
            print(e)


