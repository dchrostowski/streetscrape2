#!/bin/sh

. ./venv/bin/activate
cd ./streetscrape/
killall scrapyd
daemon --chdir=$CWD scrapyd
sleep 3
python api_scheduler.py
python ingest_gurufocus.py

# #scrapy runspider  streetscrape/spiders/swingtradebot.py
# scrapy runspider  streetscrape/spiders/thestreet.py
# scrapy runspider  streetscrape/spiders/zacks.py
# scrapy runspider  streetscrape/spiders/gurufocus.py
# python ingest_gurufocus.py

