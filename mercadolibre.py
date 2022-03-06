import dis
import requests
from bs4 import BeautifulSoup as bs
def get_offers_discount(percent_discount:int, product_type = None):
    percent_discount_offer = percent_discount
    url = ''
    items = ''
    
    cellphones_and_accessories = 'MLA1051'
    games_and_toys = 'MLA1132'
    electrical_appliance = 'MLA5726'
    consoles_and_videogames = 'MLA1144'
    
    product_list = {}
    page_counter = 1
    
    while page_counter != 9:
        if product_type == 'cellphones&accessories':
            url = 'https://www.mercadolibre.com.ar/ofertas?cat=' + cellphones_and_accessories + '&page=' + str(page_counter)
            print('Search in page: '+url)
            
        elif product_type == 'games&toys':
            url = 'https://www.mercadolibre.com.ar/ofertas?cat=' + games_and_toys + '&page=' + str(page_counter)
            print('Search in page: '+url)
            
        elif product_type == 'electricalappliance':
            url = 'https://www.mercadolibre.com.ar/ofertas?cat=' + electrical_appliance + '&page=' + str(page_counter)
            print('Search in page: '+url)
            
        elif product_type == 'consoles&videogames':
            url = 'https://www.mercadolibre.com.ar/ofertas?cat=' + consoles_and_videogames + '&page=' + str(page_counter)
            print('Search in page: '+url)
            
        else:
            url = 'https://www.mercadolibre.com.ar/ofertas'
            print('Search in page: '+url)
    
        r = requests.get(url)
        html = bs(r.text, "html.parser")
        items = html.find_all('li', {'class': 'promotion-item min'})

        product_list_with_percent_discount = []

        for item in items:
            product_title = item.find('p', {'class': 'promotion-item__title'}).getText()
            discounts_items = item.find('div', {'class': 'promotion-item__price-additional-info'}).getText()
            items_list_price_in_string = discounts_items.split('%', 1)
            
            """Deleting empty strings in items_list_price_in_string"""
            for item_price_string in items_list_price_in_string:
                if (item_price_string != ""):
                    percent_discount = int(items_list_price_in_string[0])
            
            product_dict = {'product_title': product_title, 'product_price': str(percent_discount) + '%', 'page_url': url}
            
            """List-array created for saving products data and persisting it"""
            product_list.setdefault('result', [])
            product_list['result' ].append(product_dict)

            def apply_discount(percent:int):
                """Get attribute of product in list called > result"""
                for product in product_list.items():
                    product_converted_in_list= list(product)
                    product_attributes = list(product_converted_in_list[1])
                    
                    """Parsing pricing into product_attributes and convert it in integer 
                    value for using in if statement"""
                    for prod in product_attributes:
                        product_price = prod['product_price'].split('%', 1)
                        percent_discount = int(product_price[0])
                        if percent_discount >= percent:
                            product_list_with_percent_discount.append(prod)
                    return product_list_with_percent_discount
        page_counter = page_counter + 1

    return apply_discount(percent_discount_offer)
