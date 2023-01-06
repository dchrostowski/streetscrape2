#!/bin/sh
. ../venv/bin/activate
scrapy runspider  streetscrape/spiders/swingtradebot.py
