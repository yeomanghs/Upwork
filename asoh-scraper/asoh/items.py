# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AsohItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category = scrapy.Field()
    ProductName = scrapy.Field()
    Nutrients_Comp = scrapy.Field()    
