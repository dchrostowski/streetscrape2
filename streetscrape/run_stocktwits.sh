#!/bin/sh
. ../venv/bin/activate
scrapy runspider  streetscrape/spiders/stocktwits.py
