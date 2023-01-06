#!/bin/sh
. ../venv/bin/activate
scrapy runspider  streetscrape/spiders/gurufocus.py
