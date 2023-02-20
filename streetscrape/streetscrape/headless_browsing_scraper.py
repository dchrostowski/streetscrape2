import os
import re
import json
import subprocess
from streetscrape.pipelines import StreetscrapePipeline
import time
import random




class FakeSpider():
    def __init__(self,name):
        self.name=name

class HeadlessBrowsingScraper():
    def __init__(self,spider_name):
        CWD =  os.path.dirname(os.path.abspath(__file__))
        self.js_file = os.path.join(CWD, 'headless_browsing',"%s.js" % spider_name)
        if not os.path.isfile(self.js_file):
            raise Exception("missing %s file for headless browser scraping" % self.js_file)
        self.pipeline = StreetscrapePipeline()
        self.processed_count = 0
        self.spider_name = spider_name

    def start(self):
        job = self.pipeline.get_unscrapable(self.spider_name)

        if job is None:
            print("No items left to crawl, exiting...")
            self.pipeline.cur.close()
            self.pipeline.conn.close()
            return



        if job is not None:
            self.processed_count += 1
            remaining = self.pipeline.get_unscrapable_remaining(self.spider_name)
            (url,symbol,site) = job
            if re.search('(\.com\/:?(search|etf))',url):
                print("bad url - %s, skipping." % url)
                self.pipeline.remove_unscrapable(symbol,site)
                return self.start()

            print("[%s processed, %s remaining]: fetching %s" % (self.processed_count,remaining,url))
            cmd = ['node',self.js_file,url,symbol]
            subprocess.run(cmd)
            time.sleep(random.randrange(2,20))

            data_file = "./%s_%s.json" % (self.spider_name,symbol)
            item = None

            try:
                item = json.load(open(data_file))
                print(item)
                subprocess.run(['rm', data_file])
            except FileNotFoundError as e:
                print("Data not found for %s (using url %s)" % (symbol,url))
            finally:
                self.pipeline.remove_unscrapable(symbol,self.spider_name)

            if item is not None:
                spider = FakeSpider(self.spider_name)
                self.pipeline.process_item(item,spider)

            return self.start()











