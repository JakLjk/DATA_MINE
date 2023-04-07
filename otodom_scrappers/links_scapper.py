from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4

from logger import logger

from .otodom_config import DriverConf
from custom_errors import ScrapeFailure
from support_functions.selenium_support import driver_connection_retry

def get_offer_links_from_page(page_link:str) -> list:
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)

        driver_connection_retry(driver, page_link, DriverConf.THROTTLE_REPEATS)
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)

        driver.execute_script("window.scrollTo(0,3600)")
        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        elements_no_promo = soup.find('div',  
            {"data-cy":"search.listing.organic"})

        try:
            all_link_elems = elements_no_promo.find_all("a",
                {"data-cy":"listing-item-link"})
        except AttributeError as ae:
            logger.critical("There was a problem parsing page:")
            logger.critical(page_link)
            logger.critical(f"Error: {ae}")
            raise ScrapeFailure("Unable to properly scrape this page")
        return [elem['href'] for elem in all_link_elems]