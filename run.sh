#!/bin/sh

. ./venv/bin/activate
cd ./streetscrape/
#scrapy runspider  streetscrape/spiders/swingtradebot.py
#scrapy runspider  streetscrape/spiders/thestreet.py
#scrapy runspider  streetscrape/spiders/zacks.py
scrapy runspider  streetscrape/spiders/gurufocus.py
#python ingest_gurufocus.py

