# -*- coding: utf-8 -*-
import scrapy
from pykebab.items import MenuItem

class CamelPizzaSpider(scrapy.Spider):
    name = 'camel-pizza'
    allowed_domains = ['camelpizza.pl']
    start_urls = [
        'http://camelpizza.pl/pizza',
        'http://camelpizza.pl/kebap',
        'http://camelpizza.pl/obiady',
        'http://camelpizza.pl/spaghetti',
        'http://camelpizza.pl/burgery',
        'http://camelpizza.pl/salatki',
        'http://camelpizza.pl/dla-malucha',
        'http://camelpizza.pl/zapiekanki-z-pieca-bydgoszcz-osielsko/'
    ]

    def parse(self, response):

        def get_text(td):
            return ''.join(td.css('::text').extract())

        grupa = ''.join(response.css('div#subhead').css('::text').extract()).strip()
        podgrupa = ''
        warianty = []

        for tr in response.css('div.post-entry tr'):
            pozycja = ''

            td = tr.css('td')
            liczba_komorek = len(td)
            
            if liczba_komorek >= 2:
                is_pozycja = True
                # warianty
                for j in range(1, liczba_komorek):
                    tekst = get_text(td[j])
                    if tekst.endswith(u'zł'):
                        warianty.append('')
                    else:
                        warianty.append(tekst)
                        is_pozycja = False

                if is_pozycja:
                    pozycja = get_text(td[0])
                elif not get_text(td[1]):
                    podgrupa = get_text(td[0])

                if not (is_pozycja and pozycja.strip()):
                    continue

                if podgrupa.strip():
                    pozycja = podgrupa + ' - ' + pozycja

                for j in range(1, liczba_komorek):
                    wariant = warianty[j - 1]
                    cena = get_text(td[j])

                    if 'kebap' in grupa.lower() and u'mięso' in pozycja.lower():
                        for wariant in [u'wołowina', u'kurczak']:
                            item = MenuItem(grupa = grupa, pozycja = pozycja, wariant = wariant, cena = cena)
                            yield item                    
                    else:                    
                        item = MenuItem(grupa = grupa, pozycja = pozycja, wariant = wariant, cena = cena)
                        yield item
