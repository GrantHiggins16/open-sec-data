# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecGovScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    year_dir = scrapy.Field()
    qtr_dir = scrapy.Field()
    idx_url = scrapy.Field()
    crawler_url = scrapy.Field()
    crawler_body = scrapy.Field()
