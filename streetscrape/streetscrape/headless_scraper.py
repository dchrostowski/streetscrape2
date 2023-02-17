import os
from streetscrape.pipelines import StreetscrapePipeline


class FakeSpider():
    def __init__(self,name):
        self.name=name

class HeadlessScraper():
    def __init__(self,spider_name):
        CWD =  os.path.dirname(os.path.abspath(__file__))
        self.pipeline =