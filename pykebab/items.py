# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MenuItem(scrapy.Item):
	grupa = scrapy.Field()
	pozycja = scrapy.Field()
	wariant = scrapy.Field()
	cena = scrapy.Field()