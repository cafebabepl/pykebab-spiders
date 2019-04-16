# -*- coding: utf-8 -*-
import scrapy
from pykebab.items import MenuItem

class CamelPizzaSpider(scrapy.Spider):
    name = 'camel-pizza'
    allowed_domains = ['camelpizza.pl']
    start_urls = ['https://www.camelpizza.pl/restauracja/camel-pizza-bartodzieje']

    def parse(self, response):
        def get_text(x):
            return ''.join(x.css('::text').extract()).strip()

        for groupListItem in response.css('div.m-group__list-item'):
            grupa = get_text(groupListItem.css('h3.m-list__title'))
            #print('---', grupa, '---')

            if grupa.lower() in ['sosy', 'napoje']:
                continue

            for itemRow in groupListItem.css('div.m-item__row'):
                pozycja = get_text(itemRow.css('h4.m-item__title'))
                #print("-->", pozycja)
                opis = get_text(itemRow.css('div.m-item__description'))
                addToCartButton = itemRow.css('.js-add-to-cart-button')

                if len(addToCartButton) == 1:
                    cena = get_text(addToCartButton[0])
                    if 'kebap' in grupa.lower() and u'mięso' in opis.lower():
                        for wariant in [u'wołowina', u'kurczak']:
                            item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                            #print(item)
                            yield item                    
                    else:
                        wariant = ''
                        item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                        #print(item)
                        yield item
                elif len(addToCartButton) > 1:
                    for addToCartItem in addToCartButton[1:]:
                        pola = get_text(addToCartItem).split('-')
                        wariant = pola[0].strip()
                        cena = pola[-1].strip()
                        item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                        #print(item)
                        yield item
