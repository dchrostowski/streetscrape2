# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class StreetscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SecurityItem(Item):
    symbol = Field()
    name = Field()

class ZacksItem(Item):
    symbol = Field()
    grade = Field()
    price_at_rating = Field()
    value = Field()
    growth = Field()
    momentum = Field()
    vgm = Field()
    quant = Field()

class TheStreetItem(Item):
    symbol = Field()
    grade = Field()
    price_at_rating = Field()
    quant = Field()

class GuruFocusItem(Item):
    symbol = Field()
    momentum = Field()
    value = Field()
    growth = Field()
    profitability = Field()
    balancesheet = Field()
    price_at_rating = Field()
    quant = Field()

class UnscrapableItem(Item):
    symbol = Field()
    url = Field()
    site = Field()