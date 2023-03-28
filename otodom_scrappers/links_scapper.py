from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4

from config import DriverConf
from support_functions import driver_conenction_retry

def get_offer_links_from_page(page_link):
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)
        driver_conenction_retry(driver, page_link, DriverConf.THROTTLE_REPEATS)
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)
        driver.execute_script("window.scrollTo(0,3600)")
        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        elements_no_promo = soup.find('div',  {"data-cy":"search.listing.organic"})

        try:
            all_link_elems = elements_no_promo.find_all("a", {"data-cy":"listing-item-link"})
        except Exception as err:
            # logging.critical("There was a problem parsing page:")
            # logging.critical(page_link)
            # logging.critical(f"Error: {err}")
            print(f"Error: {err}")
            return None
        return [elem['href'] for elem in all_link_elems]