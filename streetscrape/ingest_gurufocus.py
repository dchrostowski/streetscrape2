from streetscrape.pipelines import StreetscrapePipeline
import json
import os


ratings_data = json.load(open('./puppeteer/gurufocus_scores.json'))
pipeline = StreetscrapePipeline()

i = 1
for item in ratings_data:
    print("[%s of %s]" % (i,len(ratings_data)))
    print(item)
    pipeline.process_gurufocus_item(item)
    i+=1

pipeline.cur.close()
pipeline.conn.close()

#os.remove('./puppeteer/gurufocus_scores.json')
#os.remove('./gurufocus_unscrapable.json')