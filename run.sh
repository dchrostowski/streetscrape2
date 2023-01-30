#!/bin/sh

. ./venv/bin/activate
cd ./streetscrape/
scrapy runspider  streetscrape/spiders/swingtradebot.py
scrapy runspider  streetscrape/spiders/thestreet.py
scrapy runspider  streetscrape/spiders/zacks.py
scrapy runspider  streetscrape/spiders/gurufocus.py
cd puppeteer/
nvm use 16
node ./gurufocus.js
cd ../
python ingest_gurufocus.py

