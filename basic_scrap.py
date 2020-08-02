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

        self.driver.quit()
        pass
    
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
            print(links_list)
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


