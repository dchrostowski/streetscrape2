#!/bin/sh
. /home/dan/venvs/streetscrape2/bin/activate
scrapy runspider  streetscrape/streetscrape/spiders/thestreet.py
