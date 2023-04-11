from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4

from logger import logger

from .scraper_config import DriverConf
from custom_errors import ScrapeFailure
from support_functions.selenium_support import driver_connection_retry

def get_offer_links_from_page(page_link:str) -> list:
        # Running Selenium Driver, with configuration
        # from scrapper_config file
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)

        # Retrying connection in case of failure, based on settings
        # Specified in config file
        driver_connection_retry(driver, page_link, DriverConf.THROTTLE_REPEATS)
        # Sleeping in order to prevent errors thrown by site not loading completely
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)

        # TODO assure that site is porperly loaded into |page_html|
        # It is often required to use functions like:
        # "driver.execute_script("window.scrollTo(0,3600)")"
        # in order to load the whole site properly
        page_html = driver.page_source
        driver.quit()


        # TODO Add scraping logic using webpage info in |soup| variable
        # to receive last page number in range to scrape
        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        

        # TODO return list with offer links
        offer_links_on_this_page = list

        
        return offer_links_on_this_page