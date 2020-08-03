import json
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from scrap_config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    FOLDER
)
class GenerateJSONReport:
    def __init__(self, product_name, filters, base_url, currency, folder, data):
        self.product_name = product_name
        self.filters = filters
        self.base_url = base_url
        self.currency = currency
        self.data = data
        self.folder = folder
        report = {
            'title': self.product_name,
            'date': self.get_now(),
            'cheapest_item': self.get_cheapest_item(),
            'currency': self.currency,
            'filters': self.filters,
            'base_url': self.base_url,
            'products': self.data
        }
        print("[*] CREATING REPORT [*]")
        with open(f'{self.folder}/{self.product_name}.json', 'w') as f:
            json.dump(report, f)
        print("Done...")

    @staticmethod
    def get_now():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_cheapest_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("Problem with sorting items")
            return None

class MercadoLivreAPI:
    def __init__(self, product_name, filters, base_url, currency):
        self.base_url = base_url
        self.product_name = product_name
        self.currency = currency
        #filter modelling URL
        self.price_filter = f"_PriceRange_{filters['min']}-{filters['max']}"
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
    

    def run(self):
        print("[*] STARTING [*]")
        print(f"[*] Looking for {self.product_name}... [*]")
        links = self.get_products_links()
        time.sleep(2)
        print(f"[*] Got {len(links)} links to products [*]")
        products = self.get_products_info(links)
        print(f"[*] Got info  about {len(products)} products [*]")
        self.driver.quit()
        return products
    
    def get_products_info(self,link_list):
        try:
            products_info = [self.get_product_info(product_link) for product_link in link_list]
            return products_info        
        except Exception as e:
            print("[!] Error getting products info [!]")
            print(e)
            return None

    def get_product_info(self, product_link):
        self.driver.get(product_link)
        time.sleep(2)
        title = self.get_title()
        price = self.get_price()
        seller = self.get_seller()
        if title and seller and price:
            product_info = {
                'id': self.get_id(product_link),
                'title': title,
                'price': price,
                'seller': seller
            }
            return product_info
        return None

    def get_id(self, link):
        return link.split('-')[1]

    def get_seller(self):
        seller = self.driver.find_element_by_id("seller-view-more-link").get_attribute('href')
        return seller


    def get_price(self):
        price = self.driver.find_element_by_xpath("//form[@id='productInfo']/fieldset/span/span[@class='price-tag-symbol']").get_attribute('content')
        return float(price)

    def get_title(self):
        title = self.driver.find_element_by_class_name("item-title__primary").text
        return title

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath("//input[contains(@class, 'nav-search-input')]")
        element.send_keys(self.product_name)
        element.send_keys(Keys.ENTER)
        #cleaning url
        time.sleep(2)
        self.driver.get(f"http://lista.mercadolivre.com.br/{self.product_name}{self.price_filter}")
        print(f"Current URL: {self.driver.current_url}")
        time.sleep(2)
        result_list = self.driver.find_element_by_id("searchResults")
        products_id = []
        try:
            results = result_list.find_elements_by_xpath("//li/div")
            products_id = [products_id.get_attribute('id') for products_id in results]
            links_list = self.get_links(products_id)
            return links_list
 
        except Exception as e:
            print("[!] Didn't get any products... [!]")
            print(e)
            return products_id
    
    def get_links(self, id_list):
        filtered_ids = filter(lambda x: x != "", id_list)
        id_list = list(filtered_ids)
        fixed_id_list = [self.fix_id(item) for item in id_list]
        links_list = [f"https://produto.mercadolivre.com.br/{id}" for id in fixed_id_list]
        return links_list

    def fix_id(self, id):
        fixed_id = id.split("-")
        if len(fixed_id) == 1:
            fixed_id = fixed_id[0]
        else:
            fixed_id = fixed_id[1]
        fixed_id = fixed_id[:3] + '-' + fixed_id[3:] + '-_JM'      
        return fixed_id



if __name__ == '__main__':
    ml = MercadoLivreAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = ml.run()
    GenerateJSONReport(NAME,FILTERS, BASE_URL, CURRENCY, FOLDER, data)


