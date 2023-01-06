#!/bin/sh
. ../venv/bin/activate
scrapy runspider  streetscrape/spiders/thestreet.py
