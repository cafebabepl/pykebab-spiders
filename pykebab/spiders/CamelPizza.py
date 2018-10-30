# -*- coding: utf-8 -*-
import scrapy
from pykebab.items import Pozycja

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
        'http://camelpizza.pl/dla-malucha'        
    ]

    def parse(self, response):

        grupa = ''.join(response.css('div#subhead').css('::text').extract()).strip()
    
        warianty = []
        for tr in response.css('div.post-entry tr'):
            td = tr.css('td')
            c = len(td)
            
            if c >= 2:
                w = False
                for j in range(1, c):
                    t = ''.join(td[j].css('::text').extract())
                    if t.endswith(u'zł'):
                        warianty.append('')
                    else:
                        warianty.append(t)
                        w = True

                if w:
                    continue

                nazwa_pozycji = ''.join(td[0].css('::text').extract())
                if not nazwa_pozycji.strip():
                    continue;

                for j in range(1, c):
                    wariant = warianty[j - 1]
                    cena = ''.join(td[j].css('::text').extract())

                    if 'kebap' in grupa.lower() and u'mięso' in nazwa_pozycji.lower():
                        for wariant in [u'wołowina', u'kurczak']:
                            pozycja = Pozycja(grupa = grupa, nazwa = nazwa_pozycji, wariant = wariant, cena = cena)
                            yield pozycja                    
                    else:                    
                        pozycja = Pozycja(grupa = grupa, nazwa = nazwa_pozycji, wariant = wariant, cena = cena)
                        yield pozycja
            
