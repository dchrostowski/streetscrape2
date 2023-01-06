#!/bin/sh
. ../venv/bin/activate
scrapy runspider  streetscrape/spiders/zacks.py
