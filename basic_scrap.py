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
        
        time.sleep(1)
        self.driver.quit()

if __name__ == '__main__':
    ml = MercadoLivreAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    


