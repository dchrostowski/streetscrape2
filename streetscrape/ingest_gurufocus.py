
import json
import subprocess
import re
from IPython import embed
from streetscrape.pipelines import StreetscrapePipeline


#ratings_data = json.load(open('./puppeteer/gurufocus_scores.json'))
unscrapable_urls = json.load(open('./gurufocus_unscrapable.json'))
pipeline = StreetscrapePipeline()

i = 0

for url in unscrapable_urls:
    i += 1
    print("[%s of %s]: %s" % (i,len(unscrapable_urls),url))
    symbol = ''

    try:
        symbol = re.search('\/stock\/(\w+)\/summary',url).group(1) or None
    except IndexError as e:
        print("Could not extract symbol from URL %s" % url)
        continue

    subprocess.run(['node', 'gurufocus.js', url])
    data_file = "./gurufocus_%s.json" % symbol
    try:
        item = json.load(open(data_file))
        print(item)
        pipeline.process_gurufocus_item(item)

    except FileNotFoundError as e:
        print("Data for %s not found." % symbol)

    finally:
        subprocess.run(['rm', data_file])