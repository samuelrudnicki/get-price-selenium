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
        print(f"Looking for {self.product_name}...")
        links = self.get_products_links()
        time.sleep(2)
        self.driver.quit()
        pass
    
    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath("//input[contains(@class, 'nav-search-input')]")
        element.send_keys(self.product_name)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        pass


if __name__ == '__main__':
    ml = MercadoLivreAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = ml.run()


