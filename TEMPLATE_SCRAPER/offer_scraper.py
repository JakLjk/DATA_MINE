from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep

import bs4
import re

from .scraper_config import DriverConf
from support_functions.selenium_support import driver_connection_retry
from logger import logger
from custom_errors import ScrapeFailure

def get_offer_details(link: str) -> dict:
        # Running Selenium Driver, with configuration
        # from scrapper_config file
        options = Options()
        options.headless = DriverConf.HEADLESS
        driver = webdriver.Firefox(options=options)

        # In case of failed connection, driver will try to reload the site, 
        # based on time intervals specified in config.py
        driver_connection_retry(driver, link, DriverConf.THROTTLE_REPEATS)
        sleep(DriverConf.WAIT_UNTIL_PAGE_LOADED)

        # TODO assure that site is porperly loaded into |page_html|
        # It is often required to use functions like:
        # "driver.execute_script("window.scrollTo(0,3600)")"
        # in order to load the whole site properly
        page_html = driver.page_source
        driver.quit()

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        # TODO Add scraping logic, which will return dictionary
        # whith keys being column names in corresponing sql database
        # and values, which will be put in specified columns
        full_offer_info = dict

        
        return full_offer_info