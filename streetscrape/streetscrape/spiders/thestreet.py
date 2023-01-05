import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json

class ThestreetSpider(CrawlSpider):
    name = 'thestreet'
    allowed_domains = ['www.thestreet.com']

    def start_requests(self):
        with open('./thestreet_grades.csv','w') as ofh:
            ofh.write('Symbol,Company,Grade,Current Price,Quant\n')
        input_file = open('./csv/stocks.csv','r')
        lines = input_file.readlines()
        i = 0
        for line in lines:
            i += 1
            symbol = line.split(',')[0]
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
                company_name = quote['companyName'].replace(',','')
                symbol = quote['symbol']
                grade = quote['letterGradeRating']
                price = quote['currentPrice']
                quant_rating = self.calculate_quant_rating(grade)

                with open('./csv/thestreet_grades.csv','a') as ofh:
                    ofh.write("%s,%s,%s,%s,%s\n" % (symbol,company_name,grade,price,quant_rating))
        except Exception as e:
            print(e)


