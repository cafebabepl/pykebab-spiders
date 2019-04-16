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
            print('---', grupa, '---')

            if grupa.lower() in ['sosy', 'napoje']:
                continue

            for itemRow in groupListItem.css('div.m-item__row'):
                pozycja = get_text(itemRow.css('h4.m-item__title'))
                print("-->", pozycja)
                opis = get_text(itemRow.css('div.m-item__description'))
                addToCartButton = itemRow.css('.js-add-to-cart-button')

                if len(addToCartButton) == 1:
                    cena = get_text(addToCartButton[0])
                    if 'kebap' in grupa.lower() and u'mięso' in opis.lower():
                        for wariant in [u'wołowina', u'kurczak']:
                            item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                            print(item)
                            yield item                    
                    else:
                        wariant = ''
                        item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                        print(item)
                        yield item
                elif len(addToCartButton) > 1:
                    for addToCartItem in addToCartButton[1:]:
                        pola = get_text(addToCartItem).split('-')
                        wariant = pola[0].strip()
                        cena = pola[-1].strip()
                        item = MenuItem(grupa = grupa, pozycja = pozycja, opis = opis, wariant = wariant, cena = cena)
                        print(item)
                        yield item

'''
    def parse(self, response):

        def get_text(x):
            return ''.join(x.css('::text').extract()).strip()
			
        grupa = ''.join(response.css('h3.m-list__title').css('::text').extract()).strip()
        print("------------------------------------", grupa)

        grupa = 'nieznana'

        for x in response.css('div.m-item__row'):
            title = get_text(x.css('h4.m-item__title'))
            print("----------->", title)

            description = get_text(x.css('div.m-item__description'))
            ceny = x.css('.js-add-to-cart-button')

            pozycja = title
            wariant = ''

            if len(ceny) == 1:
                cena = get_text(ceny[0])
                item = MenuItem(grupa = grupa, pozycja = pozycja, wariant = wariant, cena = cena)
                print(item)
                yield item
            elif len(ceny) > 1:
                for i in range(1, len(ceny)):
                    cena = get_text(ceny[i])
                    wariant = 'wariant' + str(i)
                    item = MenuItem(grupa = grupa, pozycja = pozycja, wariant = wariant, cena = cena)
                    print(item)
                    yield item

            #xxx = len(x.css('.js-add-to-cart-button'))            
            #cena = get_text(x.css('.js-add-to-cart-button'))
'''         
            
