# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Pozycja(scrapy.Item):
	grupa = scrapy.Field()
	nazwa = scrapy.Field()
	opis = scrapy.Field()
	wariant = scrapy.Field()
	cena = scrapy.Field()