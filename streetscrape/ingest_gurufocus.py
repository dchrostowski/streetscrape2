
import json
import subprocess
import re
from streetscrape.pipelines import StreetscrapePipeline
from streetscrape.items import GuruFocusItem
from subprocess import STDOUT, check_output



pipeline = StreetscrapePipeline()

i = 0
unscrapable = pipeline.get_unscrapable('gurufocus')
pipeline.cur.close()
pipeline.conn.close()


scraped_queue = []

def empty_queue():
    if len(scraped_queue) > 1:
        pipeline = StreetscrapePipeline()
        for i in range(len(scraped_queue)):
            try:
                pipeline.process_gurufocus_item(scraped_queue.pop())
                pipeline.remove_unscrapable(symbol,site)
            except Exception as e:
                print(e)

        pipeline.cur.close()
        pipeline.conn.close()




for item in unscrapable:
    i += 1
    (url,symbol,site) = item

    if re.search('(\.com\/:?(search|etf))',url):
        continue
    print("[%s of %s]: %s" % (i,len(unscrapable),url))

    cmd = ['node','./headless_browsing/gurufocus.js']
    #output = check_output(cmd, stderr=STDOUT, timeout=10)
    subprocess.run(['node', './headless_browsing/gurufocus.js', url, symbol])
    data_file = "./gurufocus_%s.json" % symbol


    try:
        item = json.load(open(data_file))
        print(item)
        scraped_queue.append(item)
        empty_queue()

    except FileNotFoundError as e:
        print("Data for %s not found." % symbol)

    finally:
        subprocess.run(['rm', data_file])